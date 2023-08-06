import cv2
import mediapipe as mp
import time
import math

import numpy as np
from numpy import cos, sin, pi


def inside_rect(rect, num_cols, num_rows):
    # Determine if the four corners of the rectangle are inside the rectangle with width and height
    # rect tuple
    # center (x,y), (width, height), angle of rotation (to the row)
    # center  The rectangle mass center.
    # center tuple (x, y): x is regarding to the width (number of columns) of the image, y is regarding to the height (number of rows) of the image.
    # size    Width and height of the rectangle.
    # angle   The rotation angle in a clockwise direction. When the angle is 0, 90, 180, 270 etc., the rectangle becomes an up-right rectangle.
    # Return:
    # True: if the rotated sub rectangle is side the up-right rectange
    # False: else

    rect_center = rect[0]
    rect_center_x = rect_center[0]
    rect_center_y = rect_center[1]

    rect_width, rect_height = rect[1]

    rect_angle = rect[2]

    if (rect_center_x < 0) or (rect_center_x > num_cols):
        return False
    if (rect_center_y < 0) or (rect_center_y > num_rows):
        return False

    # https://docs.opencv.org/3.0-beta/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html
    box = cv2.boxPoints(rect)

    x_max = int(np.max(box[:, 0]))
    x_min = int(np.min(box[:, 0]))
    y_max = int(np.max(box[:, 1]))
    y_min = int(np.min(box[:, 1]))

    if (x_max <= num_cols) and (x_min >= 0) and (y_max <= num_rows) and (y_min >= 0):
        return True
    else:
        return False


def rect_bbx(rect):
    # Rectangle bounding box for rotated rectangle
    # Example:
    # rotated rectangle: height 4, width 4, center (10, 10), angle 45 degree
    # bounding box for this rotated rectangle, height 4*sqrt(2), width 4*sqrt(2), center (10, 10), angle 0 degree

    box = cv2.boxPoints(rect)

    x_max = int(np.max(box[:, 0]))
    x_min = int(np.min(box[:, 0]))
    y_max = int(np.max(box[:, 1]))
    y_min = int(np.min(box[:, 1]))

    # Top-left
    # (x_min, y_min)
    # Top-right
    # (x_min, y_max)
    # Bottom-left
    #  (x_max, y_min)
    # Bottom-right
    # (x_max, y_max)
    # Width
    # y_max - y_min
    # Height
    # x_max - x_min
    # Center
    # (x_min + x_max) // 2, (y_min + y_max) // 2

    center = (int((x_min + x_max) // 2), int((y_min + y_max) // 2))
    width = int(x_max - x_min)
    height = int(y_max - y_min)
    angle = 0

    return (center, (width, height), angle)


def image_rotate_without_crop(mat, angle):
    # https://stackoverflow.com/questions/22041699/rotate-an-image-without-cropping-in-opencv-in-c
    # angle in degrees

    height, width = mat.shape[:2]
    image_center = (width / 2, height / 2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1)

    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]

    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

    return rotated_mat


def crop_rectangle(image, rect):
    # rect has to be upright

    num_rows = image.shape[0]
    num_cols = image.shape[1]

    if not inside_rect(rect=rect, num_cols=num_cols, num_rows=num_rows):
        print("Proposed rectangle is not fully in the image.")
        return None

    rect_center = rect[0]
    rect_center_x = rect_center[0]
    rect_center_y = rect_center[1]
    rect_width = rect[1][0]
    rect_height = rect[1][1]

    return image[rect_center_y - rect_height // 2:rect_center_y + rect_height - rect_height // 2,
           rect_center_x - rect_width // 2:rect_center_x + rect_width - rect_width // 2]


def crop_rotated_rectangle(image, rect):
    # Crop a rotated rectangle from a image

    num_rows = image.shape[0]
    num_cols = image.shape[1]

    if not inside_rect(rect=rect, num_cols=num_cols, num_rows=num_rows):
        print("Proposed rectangle is not fully in the image.")
        return None

    rotated_angle = rect[2]

    rect_bbx_upright = rect_bbx(rect=rect)
    rect_bbx_upright_image = crop_rectangle(image=image, rect=rect_bbx_upright)

    rotated_rect_bbx_upright_image = image_rotate_without_crop(mat=rect_bbx_upright_image, angle=rotated_angle)

    rect_width = rect[1][0]
    rect_height = rect[1][1]

    crop_center = (rotated_rect_bbx_upright_image.shape[1] // 2, rotated_rect_bbx_upright_image.shape[0] // 2)

    return rotated_rect_bbx_upright_image[
           crop_center[1] - rect_height // 2: crop_center[1] + (rect_height - rect_height // 2),
           crop_center[0] - rect_width // 2: crop_center[0] + (rect_width - rect_width // 2)]

def rotate_image_from_camera(image, angle):
    # rotate an image from a camera by a given angle
    # image: image from a camera
    # angle: in degrees
    # return: rotated image
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)
    # abs_cos = abs(rotation_mat[0, 0])
    # abs_sin = abs(rotation_mat[0, 1])
    # bound_w = int(height * abs_sin + width * abs_cos)
    # bound_h = int(height * abs_cos + width * abs_sin)
    # rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    # rotation_mat[1, 2] += bound_h / 2 - image_center[1]
    rotated_mat = cv2.warpAffine(image, rotation_mat, dsize=(width, height))

    # x = int(image_center[0] - width / 2)
    # y = int(image_center[1] - height / 2)
    #
    # rotated_mat = rotated_mat[y:y + height, x:x + width]
    return rotated_mat


def rotated_rectangle(image, start_point, end_point, color, thickness, rotation=0):
    center_point = [(start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2]
    height = end_point[1] - start_point[1]
    width = end_point[0] - start_point[0]
    angle = np.radians(rotation)

    # Determine the coordinates of the 4 corner points
    rotated_rect_points = []
    x = center_point[0] + ((width / 2) * cos(angle)) - ((height / 2) * sin(angle))
    y = center_point[1] + ((width / 2) * sin(angle)) + ((height / 2) * cos(angle))
    rotated_rect_points.append([x, y])
    x = center_point[0] - ((width / 2) * cos(angle)) - ((height / 2) * sin(angle))
    y = center_point[1] - ((width / 2) * sin(angle)) + ((height / 2) * cos(angle))
    rotated_rect_points.append([x, y])
    x = center_point[0] - ((width / 2) * cos(angle)) + ((height / 2) * sin(angle))
    y = center_point[1] - ((width / 2) * sin(angle)) - ((height / 2) * cos(angle))
    rotated_rect_points.append([x, y])
    x = center_point[0] + ((width / 2) * cos(angle)) + ((height / 2) * sin(angle))
    y = center_point[1] + ((width / 2) * sin(angle)) - ((height / 2) * cos(angle))
    rotated_rect_points.append([x, y])
    # cv2.polylines(image, np.array([rotated_rect_points], np.int32), True, color, thickness)
    return rotated_rect_points



def face_detect_from_webcam(image, face_mesh):
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        start = time.time()
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
          for face_landmarks in results.multi_face_landmarks:
              left_eye_x = face_landmarks.landmark[471].x
              left_eye_y = face_landmarks.landmark[471].y
              right_eye_x = face_landmarks.landmark[473].x
              right_eye_y = face_landmarks.landmark[473].y

              shape = image.shape
              relative_left_x = int(left_eye_x * shape[1])
              relative_left_y = int(left_eye_y * shape[0])
              relative_right_x = int(right_eye_x * shape[1])
              relative_right_y = int(right_eye_y * shape[0])

              a = abs(relative_left_y - relative_right_y)
              b = abs(relative_left_x - relative_right_x)
              c = np.sqrt(a*a + b*b)

              cos_alpha = (b*b + c*c  - a*a) / (2*b*c)
              alpha = np.arccos(cos_alpha)
              alpha = int(alpha * 180 / np.pi)
              if left_eye_y > right_eye_y:
                    alpha = 360-alpha

              h, w, c = image.shape
              cx_min = w
              cy_min = h
              cx_max = cy_max = 0
              for id, lm in enumerate(face_landmarks.landmark):
                  cx, cy = int(lm.x * w), int(lm.y * h)
                  if cx < cx_min:
                      cx_min = cx
                  if cy < cy_min:
                      cy_min = cy
                  if cx > cx_max:
                      cx_max = cx
                  if cy > cy_max:
                      cy_max = cy

              cv2.rectangle(image, (cx_min, cy_min), (cx_max, cy_max), (255, 255, 0), 2)
              if 0 < cx_min < cx_max and 0 < cy_min < cy_max:
                  imag = image[cy_min:cy_max, cx_min:cx_max]
                  rotated_rect_points = rotated_rectangle(image, (cx_min, cy_min), (cx_max, cy_max), (255, 255, 0), 2,
                                                          alpha)
              else:
                  imag = image.copy()

              print(cy_min, cy_max, cx_min, cx_max)

              if alpha != None:
                img = rotate_image_from_camera(imag, alpha)
              else:
                img = rotate_image_from_camera(imag, 0)
              height, width = img.shape[:2]
              image_center = (int(width / 2), int(height / 2))
          return img


if __name__ == "__main__":
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh

    # For webcam input:
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    cap = cv2.VideoCapture(0)
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            img = face_detect_from_webcam(image, face_mesh)

            if img is None:
                img = image.copy()

            cv2.imshow('MediaPipe Face Mesh', img)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()