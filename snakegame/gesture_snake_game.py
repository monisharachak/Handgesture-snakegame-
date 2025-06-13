import cv2
import time
from camera import HandTracker
from snake_game import SnakeGame

cap = cv2.VideoCapture(0)
hand_tracker = HandTracker()
game = SnakeGame()
paused = False
game_over = False

def show_game_over_screen(frame_name, score):
    overlay = frame_name.copy()
    cv2.rectangle(overlay, (100, 100), (540, 380), (0, 0, 0), -1)
    alpha = 0.7
    cv2.addWeighted(overlay, alpha, frame_name, 1 - alpha, 0, frame_name)
    cv2.putText(frame_name, "GAME OVER", (180, 180), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
    cv2.putText(frame_name, f"Score: {score}", (240, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    cv2.putText(frame_name, "Press R to Restart", (180, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame_name, "Press ESC to Quit", (190, 340), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (game.width, game.height))
    frame = cv2.flip(frame, 1)

    if game_over:
        show_game_over_screen(frame, game.score)
        cv2.imshow("Gesture Snake Game", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            game = SnakeGame()
            game_over = False
        elif key == 27:
            break
        continue

    result = hand_tracker.detect_hands(frame)

    if result.multi_hand_landmarks:
        landmarks = result.multi_hand_landmarks[0]
        hand_tracker.draw_landmarks(frame, landmarks)

        lm = landmarks.landmark
        index_x = int(lm[8].x * game.width)
        index_y = int(lm[8].y * game.height)

        if abs(index_x - game.snake[0][0]) > abs(index_y - game.snake[0][1]):
            game.direction = 'RIGHT' if index_x > game.snake[0][0] else 'LEFT'
        else:
            game.direction = 'DOWN' if index_y > game.snake[0][1] else 'UP'

    game.move()
    if game.check_collision():
        game_over = True

    # Draw food
    cv2.rectangle(frame, tuple(game.food), (game.food[0] + 10, game.food[1] + 10), (0, 0, 255), -1)

    # Draw snake
    for segment in game.snake:
        cv2.rectangle(frame, tuple(segment), (segment[0] + 10, segment[1] + 10), (0, 255, 0), -1)

    # Draw score
    cv2.putText(frame, f"Score: {game.score}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    time.sleep(0.05)  # Slow down the loop
    cv2.imshow("Gesture Snake Game", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
