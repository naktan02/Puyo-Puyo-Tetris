import sys
# config의 HOST, PORT는 기본값으로 두고, 입력받은 값을 우선 사용합니다.
from client.config import SERVER_PORT
from client.network import ClientConnection
from client.lobby_ui import LobbyUI, LobbyState
from client.game_ui import GameUI
from client.receiver import Receiver
from client.renderer import draw_message, full_clear

def main():
    full_clear()
    print("=== 뿌요뿌요 테트리스 멀티플레이어 클라이언트 ===")
    
    # 1. 닉네임 입력
    name = input("닉네임 입력: ").strip() or "Player"
    
    # 2. 접속할 서버 IP 입력 (기본값: 로컬호스트)
    server_ip = input("서버 IP 입력 (기본값 127.0.0.1): ").strip()
    if not server_ip:
        server_ip = "127.0.0.1"
        
    print(f"[{server_ip}:{SERVER_PORT}] 서버에 접속 시도 중...")

    try:
        # 입력받은 IP로 연결 객체 생성
        conn = ClientConnection(server_ip, SERVER_PORT)
    except ConnectionRefusedError:
        print("서버에 연결할 수 없습니다. IP를 확인하거나 서버가 켜져있는지 확인하세요.")
        return

    # ... (이하 로직 동일) ...
    lobby_state = LobbyState(name)
    lobby_ui = LobbyUI(conn, lobby_state)
    lobby_ui.send_login()

    receiver = Receiver(conn, lobby_ui, lobby_state)
    receiver.start()

    while True:
        # ... (기존 루프 코드 동일)
        game_info = lobby_ui.loop()
        if game_info is None:
            break
            
        game_id, my_role, opp_name = game_info
        
        # GameUI 생성
        game_ui = GameUI(conn, game_id, lobby_state.my_id, my_role, opp_name)
        
        receiver.set_game_ui(game_ui)
        full_clear()
        game_ui.loop()
        
        # 게임 종료 후 정리
        receiver.set_game_ui(None)
        lobby_state.game_info = None
        lobby_state.game_result = None
        lobby_state.pending_from = None
        lobby_state.dirty = True
        draw_message("로비로 복귀했습니다.")

if __name__ == "__main__":
    main()