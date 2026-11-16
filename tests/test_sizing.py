from app.core.sizing import reccomended
import pytest

CHART = {
    "policy": "round_up",
    "boundary_tolerance_mm":0.3,
    "sizes": [
        {"size": "A", "width_mm": 13.0},
        {"size": "B", "width_mm": 11.0},
    ]
}

NP_CHART = {
    "policy": "nearest",
    "boundary_tolerance_mm":0.3,
    "sizes": [
        {"size": "A", "width_mm": 13.0},
        {"size": "B", "width_mm": 11.0},
    ]
}

@pytest.mark.parametrize(
          "width, chart, expected_size, expected_confidence",
          [
               (11.0,CHART,"B","high"),
               (11.0,NP_CHART,"B","high")
          ])
def test_match(width,chart,expected_size,expected_confidence):
    r = reccomended(width,chart)
    assert (r.size, r.confidence)== (expected_size, expected_confidence)

@pytest.mark.parametrize(
          "width, chart, expected_size, expected_confidence",
          [
               (11.9,CHART,"A","high"),
               (11.9,NP_CHART,"B","low")
          ])
def test_between_sizes(width,chart,expected_size,expected_confidence):
      r = reccomended(width,chart) 
      assert (r.size,r.confidence)== (expected_size, expected_confidence)

@pytest.mark.parametrize(
          "width, chart, expected_size, expected_confidence",
          [
               (15.0,CHART,None,"out_of_range"),
               (15.0,NP_CHART,None,"out_of_range")
          ])
def test_out_of_range(width, chart, expected_size, expected_confidence):
       r = reccomended(width,chart)
       assert (r.size, r.confidence)== (expected_size, expected_confidence)

@pytest.mark.parametrize(
          "width, chart, expected_size",
          [
               (10.8,CHART,"B"),
               (10.8,NP_CHART,"B")                 
          ])
def test_small_but_in_tol(width, chart, expected_size):
  
    assert reccomended(width,chart).size == (expected_size)

@pytest.mark.parametrize(
          "width, chart, expected_size, expected_confidence",
          [
               (11.4,CHART,"A","high"),
               (11.4,NP_CHART,"B","high")
          ])
def test_close_match(width, chart, expected_size, expected_confidence):
      r = reccomended(width,chart)
      assert (r.size, r.confidence)== (expected_size, expected_confidence)

@pytest.mark.parametrize(
     "width,chart,expected_size,expected_confidence",
     [
          (13.2, CHART, "A", "high"), # slightly wider than widest size
          (13.2,NP_CHART,"A","high"),
          (11.1, CHART, "A", "low"), #just over B, so B might really fit
          (11.1, NP_CHART, "B", "high"),
           (10.0, CHART, None, "out_of_range"),# below the narrowest size by more than tolerance
     ]
)

def test_edges(width,chart,expected_size,expected_confidence):
     r = reccomended(width,chart)
     assert (r.size,r.confidence) == (expected_size,expected_confidence)

def test_order_in_chart_doesnt_matter():
     chart = { **CHART,"sizes": [{"size": "B", "width_mm": 11.0}, {"size": "A", "width_mm": 13.0},  ]}
     assert reccomended(11.9,chart).size == "A"
     

def test_single_size_chart():
    chart = { **CHART,"sizes": [{"size": "A", "width_mm": 13.0},]}
    assert reccomended(13.1,chart).confidence == "high"

def test_unknown_policy_raises():
    chart = { **CHART,"policy":"up"}
    with pytest.raises(ValueError):
         reccomended(12.0,chart)