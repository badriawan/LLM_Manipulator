import display
import robot
import arena
import record
import gpt_api  # The updated gpt_api module with new functions
import static_text
import transformation  # New import for transformation functions
import random
import time
import sounddevice as sd
import numpy as np
import wave


def record_audio(filename, duration=5, fs=44100):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    print("Recording finished.")

    # Save the recording as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())


def main():
    # Initialize display
    gui = display.GUI()

    # Draw the arena
    boundaries = [(0, 0), (0, gui.height), (gui.width, gui.height), (gui.width, 0)]
    arena_space = arena.Arena(gui, boundaries)

    # Create the robot
    robot_arm = robot.Robot(gui, arena_space, link_length1= 200, link_length2=200)

    # Initialize variables
    plane = static_text.plane

    # Test move to direct coordinates
    # test_coordinates = [(968,432)]  # Test different coordinates
    # print(gui.width,gui.height)
    # for coord in test_coordinates:
    #     print(f"Moving to test coordinate: {coord}")
    #     detailed_steps, thetas = robot_arm.move(coord, "test")
    #     print("Detailed steps:", detailed_steps)
    #     print("Thetas:", thetas)

    test_coordinates = [(968,432)]  # Test different coordinates
    print(gui.width, gui.height)
    trajectory = []
    theta = []
    for coord in test_coordinates:
        # print(f"Moving to test coordinate: {coord}")
        detailed_steps, thetas = robot_arm.move(coord, "test")
        for step in detailed_steps:
            trajectory.append(step)
        for t in thetas:
            theta.append(t)
        # print("Detailed steps:", detailed_steps)
        # print("Thetas:", thetas)
    record.save_all(
        input_text=[],
        first_handle_result=[],
        target_result=[],
        trajectory_result=[],
        location_result=[],
        original_steps=[],
        detailed_steps=trajectory,
        thetas=theta
    )

    # Set up event listeners
    def on_click(event):
        # Record audio and save it as temp.wav
        audio_filename = "temp.wav"
        record_audio(audio_filename)

        # Use Whisper to transcribe audio to text
        input_text = gpt_api.speechtotext(audio_filename)

        if input_text:
            result = gpt_api.first_handle(input_text)
            print(type(result))
            print(result)
            action_type, action_detail, location = result
            print(action_type)

            original_steps = []
            target_result = []
            trajectory_result = []
            location_result = []

            if action_type == "target":
                current_position = robot_arm.end_effector_position
                positions = arena_space.get_positions(current_position)
                target_result = gpt_api.target_function(positions, action_detail)
                print(target_result)
                original_steps = target_result
            elif action_type == "pattern":
                trajectory_result = gpt_api.trajectory_function(action_detail)
                new_plane = plane.get(location)
                if new_plane:
                    transformed_trajectory = transformation.transform_coordinates(
                        trajectory_result,
                        original_plane=[(-1000, -1000), (-1000, 1000), (1000, 1000), (1000, -1000)],
                        new_plane=new_plane
                    )
                    original_steps = transformed_trajectory

            all_detailed_steps = []
            all_thetas = []

            for idx, step in enumerate(original_steps):
                detailed_steps, thetas = robot_arm.move(step, f"original_step_{idx + 1}")
                print(detailed_steps)
                all_detailed_steps.extend(detailed_steps)
                all_thetas.extend(thetas)
                # Check and remove targets if reached
                if arena_space.check_target_reached(robot_arm.end_effector_position):
                    arena_space.remove_target(robot_arm.end_effector_position)
                    robot_arm.update_gui(detailed_steps[-1])

            record.save_all(
                input_text,
                result,
                target_result,
                trajectory_result,
                location_result,
                original_steps,
                all_detailed_steps,
                all_thetas
            )

            time.sleep(0.5)  # Delay for animation effect

    def on_create_targets():
        colors = ['red', 'green', 'blue', 'yellow', 'black']  # basic 5 colors
        coordinates = static_text.reachable_grid
        selected_colors = random.sample(colors, 3)
        selected_coordinates = random.sample(coordinates, 3)
        combined_list = [(coord, color) for coord, color in zip(selected_coordinates, selected_colors)]
        # combined_list = [(coord, "black") for coord in coordinates]
        arena_space.create_targets(combined_list)
        robot_arm.update_gui()  # Ensure the robot is always drawn

    gui.set_click_listener(on_click)
    gui.set_create_targets_listener(on_create_targets)
    gui.start()


if __name__ == "__main__":
    main()
