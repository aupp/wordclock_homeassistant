# Wordclock Home Assistant Integration

This custom integration allows you to control your Raspberry Pi Wordclock from Home Assistant.

## Features

*   **Light Entity**: Control the brightness and color of the Wordclock.
*   **Plugin Switches**: Automatically discovers available plugins on your Wordclock and creates a switch for each one. Toggling a switch activates that plugin.

## Installation

1.  **Copy the Component**:
    *   Copy the `wordclock_homeassistant` folder to your Home Assistant configuration directory inside the `custom_components` folder.
    *   **Important**: Rename the folder from `wordclock_homeassistant` to `wordclock`.
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
