use std::process::exit;
use windows_volume_control::AudioController;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: vol_control <get|set|up|down|toggle-mute|max> [value]");
        exit(1);
    }

    let command = &args[1];

    unsafe {
        let mut controller = AudioController::init(None);
        controller.GetSessions();
        controller.GetDefaultAudioEnpointVolumeControl();
        controller.GetAllProcessSessions();

        let master_session = match controller.get_session_by_name("master".to_string()) {
            Some(session) => session,
            None => {
                eprintln!("Failed to get master audio session");
                exit(1);
            }
        };

        match command.as_str() {
            "get" => {
                let volume = master_session.getVolume();
                let is_muted = master_session.getMute();
                let status = if is_muted { "Muted" } else { "Unmuted" };
                println!("{:.0},{}", volume * 100.0, status);
            }
            "set" => {
                if args.len() < 3 {
                    exit(1);
                }
                let level: f32 = args[2].parse().unwrap_or(50.0);
                let level = level.clamp(0.0, 100.0) / 100.0;
                
                master_session.setVolume(level);
                println!("Volume set to {:.0}%", level * 100.0);
            }
            "up" => {
                let current_volume = master_session.getVolume();
                let new_volume = (current_volume + 0.1).min(1.0);
                master_session.setVolume(new_volume);
                println!("Volume set to {:.0}%", new_volume * 100.0);
            }
            "down" => {
                let current_volume = master_session.getVolume();
                let new_volume = (current_volume - 0.1).max(0.0);
                master_session.setVolume(new_volume);
                println!("Volume set to {:.0}%", new_volume * 100.0);
            }
            "toggle-mute" => {
                let is_muted = master_session.getMute();
                let new_mute_state = !is_muted;
                master_session.setMute(new_mute_state);
                let status = if new_mute_state { "Muted" } else { "Unmuted" };
                println!("System {}", status);
            }
            "max" => {
                master_session.setVolume(1.0);
                println!("Volume set to 100%");
            }
            _ => {
                eprintln!("Invalid command");
                exit(1);
            }
        }
    }
}
