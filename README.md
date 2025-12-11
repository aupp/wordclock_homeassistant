# Wordclock Home Assistant Integration

This custom integration allows you to control your Raspberry Pi Wordclock from Home Assistant.

## Features

*   **Light Entity**: Control the brightness and color of the Wordclock.
*   **Plugin Switches**: Automatically discovers available plugins on your Wordclock and creates a switch for each one. Toggling a switch activates that plugin.

## Installation

### Option 1: HACS (Recommended)

1.  Open HACS in Home Assistant.
2.  Go to **Integrations** > **Top right menu** > **Custom repositories**.
3.  Add the URL of this repository: `https://github.com/aupp/wordclock_homeassistant`.
4.  Select **Integration** as the category.
5.  Click **Add**.
6.  Find "Wordclock" in the list and install it.
7.  Restart Home Assistant.

### Option 2: Manual Installation

1.  **Copy the Component**:
    *   Copy the `custom_components/wordclock` folder from this repository to your Home Assistant configuration directory inside the `custom_components` folder.
    *   The final path should look like: `/config/custom_components/wordclock/`.

2.  **Restart Home Assistant**:
    *   Restart your Home Assistant instance to load the new custom component.

3.  **Add Integration**:
    *   Go to **Settings** > **Devices & Services**.
    *   Click the **+ ADD INTEGRATION** button in the bottom right.
    *   Search for "Wordclock".
    *   Select the integration.

4.  **Configuration**:
    *   Enter the **Host** (IP address or hostname) of your Wordclock.
    *   Enter the **Port** (default is usually 80 or 8080).
    *   Click **Submit**.

## Usage

Once added, you will see a device named "Wordclock" with the following entities:

*   **Light**: `light.wordclock_light` (or similar). Use this to turn the display on/off, dim it, or change the color.
*   **Switches**: `switch.wordclock_plugin_time_default`, `switch.wordclock_plugin_tetris`, etc. Turn on a switch to activate that specific mode on the clock.
