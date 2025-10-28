import cv2
import mediapipe as mp

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

def count_fingers(hand_landmarks):
    """
    Count the number of fingers extended based on the landmarks.
    For the index, middle, ring, and pinky fingers, we compare the y-coordinate
    of the fingertip with the y-coordinate of the corresponding pip joint.
    For the thumb, we compare x-coordinates (this example assumes a right hand).
    """
    finger_tip_ids = [8, 12, 16, 20]  # Tip landmarks for index, middle, ring, and pinky.
    count = 0

    # For fingers (excluding thumb)
    for tip_id in finger_tip_ids:
        tip = hand_landmarks.landmark[tip_id]
        pip = hand_landmarks.landmark[tip_id - 2]  # PIP joint landmark.
        if tip.y < pip.y:
            count += 1

    # Thumb: compare tip and ip landmarks.
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    # For a right hand, if the thumb tip is to the left of the ip joint, it's extended.
    if thumb_tip.x < thumb_ip.x:
        count += 1

    return count

# Start video capture.
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame for a mirror effect.
    frame = cv2.flip(frame, 1)

    # Convert BGR image to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands.
    results = hands.process(rgb_frame)

    # If hands are detected, process each hand.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks on the original frame.
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Count the number of extended fingers.
            finger_count = count_fingers(hand_landmarks)
            # Display the count on the frame.
            cv2.putText(frame, f'Fingers: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the result.
    cv2.imshow("Hand Tracking, Press `q` to Exit", frame)

    # Exit if 'q' is pressed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources.
cap.release()
cv2.destroyAllWindows()
