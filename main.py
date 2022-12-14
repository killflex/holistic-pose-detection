# ------------------------------------------------------------------------------------------------
# Import

import cv2
import mediapipe as mp

# ------------------------------------------------------------------------------------------------
# Set up the MediaPipe Holistic

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

cam = cv2.VideoCapture(0)
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
    ) as holistic:

    while cam.isOpened():
        success, image = cam.read()
        if not success:
            print("Ignoring Empty Camera Frame")
            continue
        
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = holistic.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        
        # FACE MESH
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style()
        )
        
        # POSE
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style()
        )
        
        cv2.imshow("Holistic Pose Cam", cv2.flip(image, 1))
        if cv2.waitKey(1) == ord('q'):
            break