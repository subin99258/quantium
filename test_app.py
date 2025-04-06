import pytest
from dash.testing.application_runners import import_app
from dash.testing.composite import DashComposite
from dash.testing.wait import wait
from selenium.webdriver.common.by import By

# Import the app
app = import_app("app")

def test_header_present(dash_duo):
    """Test that the header is present in the app."""
    # Start the app
    dash_duo.start_server(app)
    
    # Wait for the header to be present
    header = dash_duo.find_element("h1")
    
    # Assert the header text is correct
    assert header.text == "Pink Morsel Sales Dashboard"

def test_visualization_present(dash_duo):
    """Test that the visualization (line chart) is present in the app."""
    # Start the app
    dash_duo.start_server(app)
    
    # Wait for the graph to be present
    graph = dash_duo.find_element("#line-chart")
    
    # Assert the graph is present
    assert graph is not None

def test_region_picker_present(dash_duo):
    """Test that the region radio buttons are present in the app."""
    # Start the app
    dash_duo.start_server(app)
    
    # Wait for the region radio buttons to be present
    region_radio = dash_duo.find_element("#region-radio")
    
    # Assert the region radio buttons are present
    assert region_radio is not None
    
    # Verify all region options are present
    region_options = dash_duo.find_elements(By.CSS_SELECTOR, "#region-radio input[type='radio']")
    assert len(region_options) == 5  # Should have 5 options (north, east, south, west, all) 