import asyncio
import os
import re
import socket
import subprocess
import time


# =============================================================================
# CONFIG
# =============================================================================

VPNCMD = r"C:\Windows\System32\vpncmd.exe"

INPUT_FILE = "softether_servers.txt"
OUTPUT_DIR = r"D:\PROJECTS\VPN"

NIC_NAME = "VPN"
HUB_NAME = "VPNGATE"
USERNAME = "vpn"

TCP_TIMEOUT = 0.7

# Максимальное время ожидания настоящей SoftEther-сессии
VPN_TIMEOUT = 5.0

# Как часто спрашиваем AccountStatusGet
STATUS_INTERVAL = 0.5

# Таймаут отдельного вызова vpncmd
VPNCMD_TIMEOUT = 8.0


# =============================================================================
# SOFTETHER VPN CONFIG TEMPLATE
# =============================================================================

VPN_CONFIG_TEMPLATE = """# VPN Client VPN Connection Setting File
#
# This file is exported using the VPN Client Manager.
#
# This file can be imported to the VPN Client Connection Manager.

declare root
{
    bool CheckServerCert false
    uint64 CreateDateTime 0
    uint64 LastConnectDateTime 0
    bool StartupAccount false
    uint64 UpdateDateTime 0

    declare ClientAuth
    {
        uint AuthType 0
        string Username vpn
    }

    declare ClientOption
    {
        string AccountName __ACCOUNT_NAME__
        uint AdditionalConnectionInterval 1
        uint ConnectionDisconnectSpan 0
        string DeviceName VPN
        bool DisableQoS false
        bool HalfConnection false
        bool HideNicInfoWindow false
        bool HideStatusWindow false
        string Hostname __HOSTNAME__
        string HubName VPNGATE
        uint MaxConnection 1
        bool NoRoutingTracking false
        bool NoTls1 false
        bool NoUdpAcceleration false
        uint NumRetry 4294967295
        uint Port __PORT__
        uint PortUDP 0
        string ProxyName $
        byte ProxyPassword $
        uint ProxyPort 0
        uint ProxyType 0
        string ProxyUsername $
        bool RequireBridgeRoutingMode false
        bool RequireMonitorMode false
        uint RetryInterval 15
        bool UseCompress false
        bool UseEncrypt true
    }
}
"""


# =============================================================================
# HELPERS
# =============================================================================

def run_vpncmd(
    commands: list[str],
    timeout: float = VPNCMD_TIMEOUT,
) -> str:
    """
    Выполняет vpncmd localhost /client
    и передаёт команды через stdin.
    """

    input_data = "\n".join(commands) + "\n"

    try:
        result = subprocess.run(
            [
                VPNCMD,
                "localhost",
                "/client",
            ],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout,
            encoding="utf-8",
            errors="ignore",
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        return result.stdout

    except subprocess.TimeoutExpired:
        return ""

    except Exception as e:
        print(f"    vpncmd error: {e}")
        return ""


async def run_vpncmd_async(
    commands: list[str],
    timeout: float = VPNCMD_TIMEOUT,
) -> str:
    """
    Асинхронная обёртка вокруг vpncmd.
    """

    return await asyncio.to_thread(
        run_vpncmd,
        commands,
        timeout,
    )


# =============================================================================
# PARSE INPUT
# =============================================================================

def parse_servers_file(
    filepath: str = INPUT_FILE,
) -> list[tuple[str, list[int]]]:

    servers = []

    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        return []

    with open(
        filepath,
        "r",
        encoding="utf-8",
    ) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if ":" in line:

                ip_part, ports_part = line.split(
                    ":",
                    1,
                )

                ip = ip_part.strip()

                ports = []

                for p in ports_part.split(","):

                    p = p.strip()

                    if p.isdigit():

                        port = int(p)

                        if 1 <= port <= 65535:
                            ports.append(port)

            else:

                ip = line
                ports = []

            if ip:

                servers.append(
                    (
                        ip,
                        ports,
                    )
                )

    return servers


def flatten_candidates(
    servers: list[tuple[str, list[int]]],
) -> list[tuple[str, int]]:

    candidates = []

    for ip, ports in servers:

        for port in ports:

            candidates.append(
                (
                    ip,
                    port,
                )
            )

    return candidates


# =============================================================================
# UPDATE INPUT FILE
# =============================================================================

def update_servers_file(
    filepath: str,
    results: list[tuple[str, int, bool]],
):
    """
    Полностью пересобирает softether_servers.txt.

    Оставляются ТОЛЬКО реально подтверждённые IP:port.

    Пример:

        1.2.3.4:995,465,1195
        5.6.7.8:9008

    после сканирования:

        1.2.3.4:995,465

    Если у IP нет ни одного рабочего порта,
    IP полностью удаляется.

    IP без портов также удаляется, поскольку
    такой сервер невозможно подтвердить.
    """

    # -------------------------------------------------------------------------
    # Собираем только успешные результаты
    # -------------------------------------------------------------------------

    working_by_ip: dict[str, list[int]] = {}

    for ip, port, success in results:

        if not success:
            continue

        if ip not in working_by_ip:
            working_by_ip[ip] = []

        if port not in working_by_ip[ip]:
            working_by_ip[ip].append(port)

    # -------------------------------------------------------------------------
    # Сохраняем порядок IP и портов
    # -------------------------------------------------------------------------

    for ip in working_by_ip:

        working_by_ip[ip].sort()

    # -------------------------------------------------------------------------
    # Полностью перезаписываем INPUT_FILE
    # -------------------------------------------------------------------------

    try:

        with open(
            filepath,
            "w",
            encoding="utf-8",
        ) as f:

            for ip, ports in working_by_ip.items():

                if not ports:
                    continue

                f.write(
                    f"{ip}:{','.join(map(str, ports))}\n"
                )

    except Exception as e:

        print(
            f"    ERROR updating {filepath}: {e}"
        )

        return

    # -------------------------------------------------------------------------
    # Статистика
    # -------------------------------------------------------------------------

    working_count = sum(
        len(ports)
        for ports in working_by_ip.values()
    )

    print(
        f"    ✅ {filepath} rewritten"
    )

    print(
        f"    ✅ Working IPs: {len(working_by_ip)}"
    )

    print(
        f"    ✅ Working ports: {working_count}"
    )


# =============================================================================
# CLEAN OLD VPN FILES
# =============================================================================

def clean_vpn_files():
    """
    Удаляет старые .vpn файлы перед новым сканированием.

    Это предотвращает ситуацию:

        Working servers: 8
        .vpn files: 15
    """

    if not os.path.exists(OUTPUT_DIR):
        return

    removed = 0

    for name in os.listdir(OUTPUT_DIR):

        if not name.lower().endswith(".vpn"):
            continue

        path = os.path.join(
            OUTPUT_DIR,
            name,
        )

        try:

            os.remove(path)
            removed += 1

        except Exception as e:

            print(
                f"    WARNING: cannot delete {path}: {e}"
            )

    if removed:
        print(
            f"    Removed old .vpn files: {removed}"
        )


# =============================================================================
# TCP PRE-CHECK
# =============================================================================

async def tcp_check(
    ip: str,
    port: int,
) -> tuple[bool, float]:

    start = time.perf_counter()

    try:

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(
                ip,
                port,
            ),
            timeout=TCP_TIMEOUT,
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        writer.close()

        try:
            await writer.wait_closed()
        except Exception:
            pass

        return True, elapsed

    except Exception:

        elapsed = (
            time.perf_counter()
            - start
        )

        return False, elapsed


# =============================================================================
# ACCOUNT NAME
# =============================================================================

def make_account_name(
    ip: str,
    port: int,
) -> str:

    return (
        f"scan_"
        f"{ip.replace('.', '_')}_"
        f"{port}"
    )


# =============================================================================
# DELETE OLD ACCOUNT
# =============================================================================

async def delete_account(
    account: str,
):
    """
    Удаляет scanner account.

    Используется как cleanup и перед AccountCreate,
    чтобы старый account не вызывал:

        Error code: 34
        VPN Connection Setting with the specified name already exists.
    """

    await run_vpncmd_async(
        [
            f"AccountDisconnect {account}",
            f"AccountDelete {account}",
        ],
        timeout=VPNCMD_TIMEOUT,
    )


# =============================================================================
# CREATE SOFTETHER ACCOUNT
# =============================================================================

async def create_account(
    account: str,
    ip: str,
    port: int,
) -> bool:

    # -------------------------------------------------------------------------
    # Удаляем старый scanner account
    # -------------------------------------------------------------------------

    await delete_account(account)

    command = (
        f"AccountCreate {account} "
        f"/SERVER:{ip}:{port} "
        f"/HUB:{HUB_NAME} "
        f"/USERNAME:{USERNAME} "
        f"/NICNAME:{NIC_NAME}"
    )

    output = await run_vpncmd_async(
        [command],
        timeout=VPNCMD_TIMEOUT,
    )

    if "The command completed successfully" in output:
        return True

    # Некоторые версии vpncmd могут отличаться выводом.
    if (
        "Error occurred" not in output
        and "Command not found" not in output
        and "failed" not in output.lower()
    ):
        if "AccountCreate command" in output:
            return True

    print("    AccountCreate failed:")
    print(output)

    return False


# =============================================================================
# CONNECT
# =============================================================================

async def connect_account(
    account: str,
) -> bool:

    output = await run_vpncmd_async(
        [
            f"AccountConnect {account}"
        ],
        timeout=VPNCMD_TIMEOUT,
    )

    if "The command completed successfully" in output:
        return True

    print("    AccountConnect failed:")
    print(output)

    return False


# =============================================================================
# GET ACCOUNT STATUS
# =============================================================================

async def get_account_status(
    account: str,
) -> str | None:

    output = await run_vpncmd_async(
        [
            f"AccountStatusGet {account}"
        ],
        timeout=VPNCMD_TIMEOUT,
    )

    if not output:
        return None

    match = re.search(
        r"Session Status\s*\|\s*(.+)",
        output,
        re.IGNORECASE,
    )

    if match:

        status = match.group(1).strip()

        return status

    return None


# =============================================================================
# DISCONNECT
# =============================================================================

async def disconnect_account(
    account: str,
):
    await run_vpncmd_async(
        [
            f"AccountDisconnect {account}"
        ],
        timeout=VPNCMD_TIMEOUT,
    )


# =============================================================================
# REAL SOFTETHER TEST
# =============================================================================

async def real_softether_test(
    ip: str,
    port: int,
) -> tuple[bool, float | None, str]:

    account = make_account_name(
        ip,
        port,
    )

    print(
        f"    Account: {account}"
    )

    # -------------------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------------------

    print(
        "    Creating account..."
    )

    created = await create_account(
        account,
        ip,
        port,
    )

    if not created:

        return (
            False,
            None,
            "AccountCreate failed",
        )

    start = time.perf_counter()

    try:

        # ---------------------------------------------------------------------
        # CONNECT
        # ---------------------------------------------------------------------

        print(
            "    Connecting..."
        )

        connected = await connect_account(
            account
        )

        if not connected:

            return (
                False,
                None,
                "AccountConnect failed",
            )

        print(
            f"    Waiting {VPN_TIMEOUT:.1f}s max..."
        )

        # ---------------------------------------------------------------------
        # POLLING
        # ---------------------------------------------------------------------

        last_status = None

        while True:

            elapsed = (
                time.perf_counter()
                - start
            )

            if elapsed >= VPN_TIMEOUT:
                break

            status = await get_account_status(
                account
            )

            if status and status != last_status:

                print(
                    f"    Status: {status}"
                )

                last_status = status

            # =================================================================
            # ONLY SUCCESS CONDITION
            # =================================================================

            if status:

                normalized = status.lower()

                if (
                    "connection completed"
                    in normalized
                    and
                    "session established"
                    in normalized
                ):

                    latency = (
                        time.perf_counter()
                        - start
                    ) * 1000

                    return (
                        True,
                        round(latency, 1),
                        status,
                    )

            # -----------------------------------------------------------------
            # Immediate failure statuses
            # -----------------------------------------------------------------

            if status:

                normalized = status.lower()

                failure_markers = (
                    "connection failed",
                    "offline",
                    "authentication failed",
                    "connection error",
                    "disconnecting",
                )

                if any(
                    marker in normalized
                    for marker in failure_markers
                ):

                    return (
                        False,
                        None,
                        status,
                    )

            await asyncio.sleep(
                STATUS_INTERVAL
            )

        return (
            False,
            None,
            "TIMEOUT",
        )

    finally:

        # ---------------------------------------------------------------------
        # ALWAYS CLEAN UP
        # ---------------------------------------------------------------------

        print(
            "    Disconnecting..."
        )

        await disconnect_account(
            account
        )

        await asyncio.sleep(
            0.2
        )

        print(
            "    Deleting account..."
        )

        await delete_account(
            account
        )


# =============================================================================
# CREATE VPN FILE
# =============================================================================

def create_vpn_file(
    ip: str,
    port: int,
) -> str | None:

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    account_name = make_account_name(
        ip,
        port,
    )

    file_path = os.path.join(
        OUTPUT_DIR,
        f"VPN_{ip}_{port}.vpn",
    )

    content = (
        VPN_CONFIG_TEMPLATE
        .replace(
            "__ACCOUNT_NAME__",
            account_name,
        )
        .replace(
            "__HOSTNAME__",
            ip,
        )
        .replace(
            "__PORT__",
            str(port),
        )
    )

    try:

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as f:

            f.write(content)

        return file_path

    except Exception as e:

        print(
            f"    ERROR creating .vpn: {e}"
        )

        return None


# =============================================================================
# TEST ONE CANDIDATE
# =============================================================================

async def test_candidate(
    index: int,
    total: int,
    ip: str,
    port: int,
) -> tuple[str, int, bool]:

    print()
    print(
        f"[{index}/{total}]"
    )
    print(
        "-" * 80
    )
    print(
        f"TEST: {ip}:{port}"
    )

    # =========================================================================
    # TCP PRE-CHECK
    # =========================================================================

    tcp_open, tcp_time = await tcp_check(
        ip,
        port,
    )

    if not tcp_open:

        print(
            f"    ⚫ TCP CLOSED "
            f"({tcp_time:.2f}s)"
        )

        print(
            f"    ❌ FAILED: {ip}:{port}"
        )

        return (
            ip,
            port,
            False,
        )

    print(
        f"    🟡 TCP OPEN "
        f"({tcp_time:.2f}s)"
    )

    # =========================================================================
    # REAL SOFTETHER TEST
    # =========================================================================

    success, latency, status = (
        await real_softether_test(
            ip,
            port,
        )
    )

    if success:

        print()

        print(
            "    🟢 CONFIRMED SOFTETHER"
        )

        print(
            f"    Session: {status}"
        )

        if latency is not None:

            print(
                f"    Connection time: "
                f"{latency:.1f} ms"
            )

        # ---------------------------------------------------------------------
        # ONLY NOW CREATE VPN FILE
        # ---------------------------------------------------------------------

        vpn_file = create_vpn_file(
            ip,
            port,
        )

        if vpn_file:

            print(
                "    ✅ .vpn CREATED:"
            )

            print(
                f"       {vpn_file}"
            )

        print(
            f"    ✅ WORKING: {ip}:{port}"
        )

        return (
            ip,
            port,
            True,
        )

    # =========================================================================
    # FAILED
    # =========================================================================

    print(
        f"    🔴 NOT CONFIRMED: {status}"
    )

    print(
        f"    ❌ FAILED: {ip}:{port}"
    )

    return (
        ip,
        port,
        False,
    )


# =============================================================================
# MAIN
# =============================================================================

async def main():

    print(
        "=" * 80
    )

    print(
        "SOFTETHER FAST REAL SERVER SCANNER"
    )

    print(
        "=" * 80
    )

    print(
        f"vpncmd       : {VPNCMD}"
    )

    print(
        f"Input        : {INPUT_FILE}"
    )

    print(
        f"Output       : {OUTPUT_DIR}"
    )

    print(
        f"TCP timeout  : {TCP_TIMEOUT}s"
    )

    print(
        f"VPN timeout  : {VPN_TIMEOUT}s"
    )

    print(
        f"Status check : {STATUS_INTERVAL}s"
    )

    print(
        "Detection    : "
        "TCP → REAL SOFTETHER SESSION"
    )

    print(
        "=" * 80
    )

    # =========================================================================
    # CHECK VPNCMD
    # =========================================================================

    if not os.path.exists(VPNCMD):

        print()

        print(
            "ERROR: vpncmd not found:"
        )

        print(
            VPNCMD
        )

        return

    # =========================================================================
    # LOAD SERVERS
    # =========================================================================

    servers = parse_servers_file(
        INPUT_FILE
    )

    if not servers:

        print()

        print(
            "No servers found."
        )

        return

    candidates = flatten_candidates(
        servers
    )

    print()

    print(
        f"Servers:    {len(servers)}"
    )

    print(
        f"Candidates: {len(candidates)}"
    )

    print()

    # =========================================================================
    # CLEAN OLD VPN FILES
    # =========================================================================

    print(
        "Cleaning old .vpn files..."
    )

    clean_vpn_files()

    # =========================================================================
    # RESULTS
    # =========================================================================

    working = []
    results = []

    # =========================================================================
    # TEST SEQUENTIALLY
    # =========================================================================

    start_total = time.perf_counter()

    for index, (ip, port) in enumerate(
        candidates,
        start=1,
    ):

        result = await test_candidate(
            index,
            len(candidates),
            ip,
            port,
        )

        result_ip, result_port, success = result

        # ---------------------------------------------------------------------
        # Сохраняем результат каждого кандидата
        # ---------------------------------------------------------------------

        results.append(result)

        if success:

            working.append(
                (
                    result_ip,
                    result_port,
                )
            )

    elapsed_total = (
        time.perf_counter()
        - start_total
    )

    # =========================================================================
    # UPDATE INPUT FILE
    # =========================================================================

    print()

    print(
        "=" * 80
    )

    print(
        "UPDATING SERVER LIST"
    )

    print(
        "=" * 80
    )

    update_servers_file(
        INPUT_FILE,
        results,
    )

    # =========================================================================
    # SAVE WORKING SERVERS
    # =========================================================================

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    list_file_path = os.path.join(
        OUTPUT_DIR,
        "working_servers.txt",
    )

    with open(
        list_file_path,
        "w",
        encoding="utf-8",
    ) as f:

        for ip, port in working:

            f.write(
                f"{ip}:{port}\n"
            )

    # =========================================================================
    # SUMMARY
    # =========================================================================

    vpn_files = [
        name
        for name in os.listdir(OUTPUT_DIR)
        if name.lower().endswith(".vpn")
    ]

    print()

    print(
        "=" * 80
    )

    print(
        "SCAN FINISHED"
    )

    print(
        "=" * 80
    )

    print(
        f"Candidates tested: {len(candidates)}"
    )

    print(
        f"Working servers:   {len(working)}"
    )

    print(
        f".vpn files:        {len(vpn_files)}"
    )

    print(
        f"Elapsed time:      {elapsed_total:.1f}s"
    )

    print(
        f"Working list:      {list_file_path}"
    )

    print(
        f"Updated input:     {INPUT_FILE}"
    )

    print(
        "=" * 80
    )

    if working:

        print()

        print(
            "CONFIRMED SERVERS:"
        )

        for ip, port in working:

            print(
                f"  🟢 {ip}:{port}"
            )

    else:

        print()

        print(
            "No SoftEther servers confirmed."
        )


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print()

        print(
            "Scanner interrupted by user."
        )