from board import *
import sbs

clients = [0]

class TicTacToe:
    missionState = "blank"
    board = Board()

    def render(sim, clientID):
        
        state =  TicTacToe.board.check_winner()

        if state == EndGame.UNKNOWN:
            sbs.send_gui_clear(clientID)
            TicTacToe.missionState = "mission_options"
            for index, p in enumerate(TicTacToe.board.grid):
                x = (index % 3) * 10 + 30 + 15
                y = index//3  * 10 + 30 +15
                if p == Turn.X_TURN:
                    sbs.send_gui_text(clientID, "X", f"text{index}", x, y, x+10,y+10)
                elif p == Turn.O_TURN:
                    sbs.send_gui_text(clientID, "O", f"text{index}", x, y, x+10,y+10)
                elif TicTacToe.board.turn == Turn.X_TURN and clientID==clients[0]:
                    sbs.send_gui_button(clientID, f"{index+1}", f"{index}", x, y, x+10,y+10)
                elif TicTacToe.board.turn == Turn.O_TURN and clientID==clients[1]:
                    sbs.send_gui_button(clientID, f"{index+1}", f"{index}", x, y, x+10,y+10)
                else:
                    sbs.send_gui_text(clientID, "?", f"text{index}", x, y, x+10,y+10)
        elif state == EndGame.X_WINS:
            sbs.send_gui_clear(clientID)
            sbs.send_gui_text(clientID, "X WINS ", "text", 50, 50, 60,60)
            if clientID == 0:
                sbs.send_gui_button(clientID, f"Play Again", f"replay", 80, 80, 90,90)
        elif state == EndGame.O_WINS:
            sbs.send_gui_clear(clientID)
            sbs.send_gui_text(clientID, "O WINS ", "text", 50, 50, 60,60)
            if clientID == 0:
                sbs.send_gui_button(clientID, f"Play Again", f"replay", 80, 80, 90,90)
        elif state == EndGame.DRAW:
            sbs.send_gui_clear(clientID)
            sbs.send_gui_text(clientID, "DRAW", "text", 50, 50, 60,60)
            if clientID == 0:
                sbs.send_gui_button(clientID, f"Play Again", f"replay", 80, 80, 90,90)



    def update(sim , message_tag, clientID):
        if "replay" == message_tag:
            TicTacToe.board.clear()
        else:
            slot = int(message_tag)
            TicTacToe.board.set_grid(slot)



def  HandlePresentGUI(sim):
    global clients
    if len(clients) < 2:
        sbs.send_gui_text(0, "Waiting for player", "wait", 50, 50, 60,60)
    else:
        for i in clients:
            TicTacToe.render(sim, i)

########################################################################################################
def  HandlePresentGUIMessage(sim, message_tag, clientID):
    TicTacToe.update(sim, message_tag, clientID)
    TicTacToe.render(sim, clientID)

# Part Two
def  HandleClientConnect(sim, clientID):
    global clients
    clients.append(clientID)
    HandlePresentGUI(sim)
