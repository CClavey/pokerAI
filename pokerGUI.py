import cv2
import Cards

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load the train rank and suit images
path = "/Users/cole/PycharmProjects/pokerAI/Card_Imgs"
train_ranks = Cards.load_ranks(path)
train_suits = Cards.load_suits(path)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Pre-process camera image (gray, blur, and threshold it)
    pre_proc = Cards.preprocess_image(frame)

    # Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)

    # If there are no contours, do nothing
    if len(cnts_sort) != 0:
        cards = []

        for i in range(len(cnts_sort)):
            if cnt_is_card[i] == 1:
                cards.append(Cards.preprocess_card(cnts_sort[i], frame))

                # Find the best rank and suit match for the card.
                cards[-1].best_rank_match, cards[-1].best_suit_match, cards[-1].rank_diff, cards[-1].suit_diff = Cards.match_card(cards[-1], train_ranks, train_suits)

                # Draw center point and match result on the image.
                frame = Cards.draw_results(frame, cards[-1])

        # Draw card contours on the image
        if len(cards) != 0:
            temp_cnts = [card.contour for card in cards]
            cv2.drawContours(frame, temp_cnts, -1, (255, 0, 0), 2)

    # Display the frame
    cv2.imshow('Webcam with Card Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
