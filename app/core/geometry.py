import cv2, numpy as np

CARD_W_MM = 85.60
CARD_H_MM = 53.98
GRID = 10 # grid units per milimeter

def _area(points: np.ndarray) -> float:
    x,y = points[:,0], points[:,1]

    return 0.5 * abs(np.dot(x,np.roll(y,-1)) - np.dot(y,np.roll(x,-1)))

"""Perspective transform from photo pixels to the card's plane (grid units)"""
def card_homography(corners):
    src = np.array(corners,dtype=np.float32)
    if src.shape != (4,2):
        raise ValueError("Exactly 4 (x,y) corner points are required")
    if _area(src) < 100:
        raise ValueError("Card corners are too close together or in a line")
    dst = np.array(
        [
            [0,0],
            [CARD_W_MM * GRID, 0],
            [CARD_W_MM * GRID, CARD_H_MM * GRID],
            [0,CARD_H_MM * GRID]
        ],
        dtype=np.float32,
    )
    return cv2.getPerspectiveTransform(src,dst)

def to_card_plane(H,points):
    pts = np.array(points,dtype=np.float32).reshape(-1,1,2)
    return cv2.perspectiveTransform(pts,H).reshape(-1,2)

def width_mm(H,left,right,bias_factor:float =1.0) -> float:
    a,b = to_card_plane(H,[left,right])
    return float(np.linalg.norm(a-b))/ GRID * bias_factor 