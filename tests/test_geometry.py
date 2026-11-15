import  cv2, numpy as np, pytest

from app.core.geometry import card_homography,width_mm

def test_axis_aligned_card():
    # card appears at 5 pixels/mm
    corners = [(0,0),(428,0),(428,269.9),(0,269.9)]

    H = card_homography(corners)

    assert width_mm(H, (0,0),(50,0)) == pytest.approx(10.0, abs=0.05)

def test_perspective_recovers_width():
    metric = np.float32([[0, 0], [85.6, 0], [85.6, 53.98], [0, 53.98]])
    photo = np.float32([[100, 120], [620, 90], [660, 430], [80, 400]])

    M = cv2.getPerspectiveTransform(metric,photo)

    def project(p):
        v = M @ np.array([p[0],p[1],1.0])
        return (v[0]/ v[2], v[1]/v[2])
    
    corners = [project(p) for p in metric]
    H = card_homography(corners)
    left, right = project((20,60)), project((32,60)) #12mm apart

    assert width_mm(H, left, right) == pytest.approx(12.0, abs=0.05)


def test_rejects_wrong_corner_count():
    with pytest.raises(ValueError):
        card_homography([(0,0),(1,0),(1,1)])

def test_rejects_degenerate_corners():
    with pytest.raises(ValueError):
        card_homography([(0,0),(1,0),(2,0),(3,0)])
        
