import os
import sys

# --- 화면 제어 함수 ---
BLOCK_SHAPES = {
    "I": ["    ", "####", "    ", "    "],
    "O": [" ## ", " ## ", "    ", "    "],
    "T": [" #  ", "### ", "    ", "    "],
    "S": [" ## ", "##  ", "    ", "    "],
    "Z": ["##  ", " ## ", "    ", "    "],
    "J": ["#   ", "### ", "    ", "    "],
    "L": ["  # ", "### ", "    ", "    "],
    "":  ["    ", "    ", "    ", "    "] # 공백
}

def clear_screen():
    """커서를 상단으로 이동 (깜빡임 최소화)"""
    print("\033[H", end="")

def full_clear():
    """화면 전체 지우기 (로비 진입 시 등)"""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- 그리기 함수 ---

def draw_header(title: str):
    print("=" * 40)
    print(f"{title:^40}") # 가운데 정렬
    print("=" * 40)

def draw_lobby(my_id: int | None, name: str, users: list[tuple[int, str]]):
    # 버퍼링: 문자열을 모아서 한 번에 출력
    buffer = []
    
    # 헤더
    buffer.append("=" * 40)
    buffer.append(f"{'뿌요뿌요 테트리스 - 로비':^40}")
    my_info = f"(나: {name}#{my_id})" if my_id else ""
    buffer.append(f"{my_info:^40}")
    buffer.append("=" * 40 + "\n")

    buffer.append("[ 접속자 목록 ]")
    if not users:
        buffer.append("  (없음)")
    else:
        for idx, (uid, uname) in enumerate(users, 1):
            me = " (나)" if my_id == uid else ""
            buffer.append(f"  {idx}. [{uid}] {uname}{me}")
    
    buffer.append("\n" + "-" * 40)
    buffer.append("[명령] 번호: 대결신청 | q: 종료")
    
    clear_screen()
    print("\n".join(buffer))

def draw_message(msg: str):
    print(f"\n[알림] {msg}")

def draw_game(
    my_role: str,
    opponent_name: str,
    scores: dict,
    my_board: list,
    op_board: list,
    my_next: str,   # 추가됨
    op_next: str,   # 추가됨
    game_over_msg: str | None = None,
):
    my_score = scores.get(my_role, 0)
    op_role = 'P2' if my_role == 'P1' else 'P1'
    op_score = scores.get(op_role, 0)

    buffer = []
    
    # 1. 상단 헤더
    buffer.append("=" * 70)
    title = f"ME({my_role}) {my_score} VS {op_score} OPP({opponent_name})"
    buffer.append(f"{title:^70}")
    buffer.append("-" * 70)
    
    # 2. 보드 + NEXT 블록 그리기
    # 구조: | 내보드 |  NEXT  | 상대보드 |
    
    # Next 블록 모양 가져오기
    my_next_shape = BLOCK_SHAPES.get(my_next, BLOCK_SHAPES[""])
    op_next_shape = BLOCK_SHAPES.get(op_next, BLOCK_SHAPES[""])
    
    for r in range(20):
        # 내 보드 한 줄
        row_my = "".join(my_board[r])
        # 상대 보드 한 줄
        row_op = "".join(op_board[r])
        
        # 중앙 정보창 (NEXT 블록 표시)
        center_txt = "      "
        if r == 1:
            center_txt = " NEXT "
        elif 2 <= r <= 5:
            # 내 NEXT 블록 그리기
            center_txt = f" {my_next_shape[r-2]} " 
        
        # 문자열 합치기
        line = f"|{row_my}|{center_txt}|{row_op}|"
        
        # 상대방 NEXT도 보여주고 싶다면? (선택사항)
        if r == 1:
            line += " OP-NEXT"
        elif 2 <= r <= 5:
            line += f"  {op_next_shape[r-2]}"
            
        buffer.append(line)
    
    buffer.append("=" * 70)

    if game_over_msg:
        buffer.append(f"\n>>> {game_over_msg} <<<")
    else:
        buffer.append("\n[조작] WASD/IJKL:이동 | Space:드롭 | Q:기권")

    clear_screen()
    print("\n".join(buffer))