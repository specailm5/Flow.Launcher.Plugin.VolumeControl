import os
import subprocess
from pyflowlauncher import Plugin, Result, send_results
from pyflowlauncher.result import ResultResponse

plugin = Plugin()

def get_current_volume_status(executable_path):
    """Get current volume and mute status"""
    try:
        process = subprocess.run([executable_path, "get"], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output = process.stdout.strip()
        if ',' in output:
            volume, status = output.split(',', 1)
            is_muted = status.lower() == "muted"
            return int(volume), is_muted
        return 50, False
    except:
        return 50, False

@plugin.on_method
def query(query: str) -> ResultResponse:
    """Process query and return results"""
    try:
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        executable_path = os.path.join(plugin_dir, "vol_control.exe")

        results = []
        
        if not os.path.exists(executable_path):
            error_result = Result(
                Title="Error: vol_control.exe not found",
                SubTitle="Please ensure the Rust executable is in the plugin directory.",
                IcoPath="Images/icon.png"
            )
            return send_results([error_result])

        parts = query.strip().lower().split() if query else []
        
        current_volume, is_muted = get_current_volume_status(executable_path)

        if not parts:

            results = []
            
            status_text = "Muted" if is_muted else "Unmuted"
            volume_result = Result(
                Title=f"Current Volume: {current_volume}%",
                SubTitle=status_text,
                IcoPath="Images/icon.png"
            )
            results.append(volume_result)
            
            if is_muted:
                mute_result = Result(
                    Title="Unmute",
                    SubTitle="Click to unmute the system",
                    IcoPath="Images/icon.png",
                    JsonRPCAction={
                        "method": "execute_volume_command",
                        "parameters": ["toggle-mute", ""]
                    }
                )
            else:
                mute_result = Result(
                    Title="Mute",
                    SubTitle="Click to mute the system",
                    IcoPath="Images/icon.png",
                    JsonRPCAction={
                        "method": "execute_volume_command",
                        "parameters": ["toggle-mute", ""]
                    }
                )
            results.append(mute_result)
            
            return send_results(results)
            
        elif len(parts) == 1:

            if parts[0] in ["mute", "unmute"]:

                if parts[0] == "mute" and not is_muted:

                    result = Result(
                        Title="Mute System",
                        SubTitle="Click to mute the system",
                        IcoPath="Images/icon.png",
                        JsonRPCAction={
                            "method": "execute_volume_command",
                            "parameters": ["toggle-mute", ""]
                        }
                    )
                elif parts[0] == "unmute" and is_muted:

                    result = Result(
                        Title="Unmute System",
                        SubTitle="Click to unmute the system",
                        IcoPath="Images/icon.png",
                        JsonRPCAction={
                            "method": "execute_volume_command",
                            "parameters": ["toggle-mute", ""]
                        }
                    )
                elif parts[0] == "mute" and is_muted:

                    result = Result(
                        Title="System Already Muted",
                        SubTitle="Type 'unmute' to unmute the system",
                        IcoPath="Images/icon.png",
                        JsonRPCAction={
                            "method": "execute_volume_command",
                            "parameters": ["toggle-mute", ""]
                        }
                    )
                else:

                    result = Result(
                        Title="System Already Unmuted",
                        SubTitle="Type 'mute' to mute the system",
                        IcoPath="Images/icon.png",
                        JsonRPCAction={
                            "method": "execute_volume_command",
                            "parameters": ["toggle-mute", ""]
                        }
                    )
                return send_results([result])
            elif parts[0] in ["up", "down", "max"]:

                cmd_action = parts[0]
                result = Result(
                    Title=f"Execute: {parts[0]}",
                    SubTitle=f"Click to {parts[0]} volume",
                    IcoPath="Images/icon.png",
                    JsonRPCAction={
                        "method": "execute_volume_command",
                        "parameters": [cmd_action, ""]
                    }
                )
                return send_results([result])
            elif parts[0].isdigit():

                result = Result(
                    Title=f"Set volume to {parts[0]}%",
                    SubTitle=f"Click to set volume to {parts[0]}%",
                    IcoPath="Images/icon.png",
                    JsonRPCAction={
                        "method": "execute_volume_command",
                        "parameters": ["set", parts[0]]
                    }
                )
                return send_results([result])
            else:

                mute_title = "Unmute" if is_muted else "Mute"
                mute_subtitle = f"Click to {mute_title.lower()} the system"
                
                suggestions = [
                    (mute_title, mute_subtitle),
                    ("up", "Increase volume by 10%"),
                    ("down", "Decrease volume by 10%"),
                    ("max", "Set volume to 100%"),
                    ("0-100", "e.g., 'vol 75' to set a specific volume")
                ]
                results = []
                for title, subtitle in suggestions:
                    result = Result(
                        Title=title,
                        SubTitle=subtitle,
                        IcoPath="Images/icon.png"
                    )

                    if title in ["Mute", "Unmute", "up", "down", "max"]:
                        if title in ["Mute", "Unmute"]:
                            cmd_action = "toggle-mute"
                        else:
                            cmd_action = title.lower()
                        result.JsonRPCAction = {
                            "method": "execute_volume_command",
                            "parameters": [cmd_action, ""]
                        }
                    results.append(result)
                return send_results(results)
        else:

            current_volume, is_muted = get_current_volume_status()
            
            if current_volume is not None:
                if is_muted:
                    status_text = f"Current Volume: {current_volume}% (Muted)"
                    help_text = "System is muted. Use 'mute' to unmute, or try 'up', 'down', 'max', or a number (0-100)"
                else:
                    status_text = f"Current Volume: {current_volume}%"
                    help_text = "Try: 'mute', 'up', 'down', 'max', or enter a number (0-100)"
            else:
                status_text = "Volume Control"
                help_text = "Try: 'mute', 'up', 'down', 'max', or enter a number (0-100)"
            
            result = Result(
                Title=status_text,
                SubTitle=help_text,
                IcoPath="Images/icon.png"
            )
            return send_results([result])
        
    except Exception as e:
        error_result = Result(
            Title=f"Plugin Error: {str(e)}",
            SubTitle="Volume control plugin encountered an error",
            IcoPath="Images/icon.png"
        )
        return send_results([error_result])

@plugin.on_method
def execute_volume_command(cmd: str, arg: str = "") -> ResultResponse:
    """Execute volume control command"""
    try:
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        executable_path = os.path.join(plugin_dir, "vol_control.exe")
        
        if not os.path.exists(executable_path):
            error_result = Result(
                Title="Error: vol_control.exe not found",
                SubTitle="Please ensure the Rust executable is in the plugin directory.",
                IcoPath="Images/icon.png"
            )
            return send_results([error_result])
        
        full_command = [executable_path, cmd]
        if arg:
            full_command.append(arg)
        
        process = subprocess.run(full_command, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        result = Result(
            Title="Volume command executed",
            SubTitle=process.stdout.strip() if process.stdout.strip() else f"Successfully executed: {cmd} {arg}".strip(),
            IcoPath="Images/icon.png"
        )
        return send_results([result])
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Command failed"
        error_result = Result(
            Title="Error executing command",
            SubTitle=error_msg,
            IcoPath="Images/icon.png"
        )
        return send_results([error_result])
    except Exception as e:
        error_result = Result(
            Title="An unexpected error occurred",
            SubTitle=str(e),
            IcoPath="Images/icon.png"
        )
        return send_results([error_result])

if __name__ == "__main__":
    plugin.run()
