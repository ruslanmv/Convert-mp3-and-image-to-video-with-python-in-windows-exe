from pathlib import Path
import subprocess
import platform

from gooey import Gooey, GooeyParser


@Gooey(dump_build_config=False, program_name="Audio to Video Conversion Tool")
def main():
    desc = "A Python GUI App to convert a .mp3 and an image into a .mp4"
    mp3_select_help_msg = "Select a .mp3 audio file to process"
    image_select_help_msg = "Select an image file (.png or .jpg) to use in the video"

    my_parser = GooeyParser(description=desc)
    my_parser.add_argument(
        "mp3_to_convert", help=mp3_select_help_msg, widget="FileChooser"
    )
    my_parser.add_argument(
        "image_to_convert", help=image_select_help_msg, widget="FileChooser"
    )
    my_parser.add_argument(
        "output_dir", help="Directory to save output", widget="DirChooser"
    )

    args = my_parser.parse_args()

    # construct the .mp3 input audio file path
    mp3_to_convert_Path = Path(args.mp3_to_convert)

    # construct image file path
    image_to_convert_Path = Path(args.image_to_convert)

    mp4_outfile_name = str(mp3_to_convert_Path.stem) + "_video.mp4"
    mp4_outfile_Path = Path(args.output_dir, mp4_outfile_name)
    mp4_outfile_Path.unlink(missing_ok=True) # delete the .mp4 file if it's there

    # Determine ffmpeg executable file path
    """
    where ffmpeg
    """
    if platform.system() == 'Windows':

        ffmpeg_path_bytes = subprocess.check_output("where ffmpeg", shell=True) 
        
    elif platform.system() == 'Linux':
        ffmpeg_path_bytes = subprocess.check_output("which ffmpeg", shell=True) 

    ffmpeg_executable_path = ffmpeg_path_bytes.decode().strip()
    print("ffmpeg_executable_path: ", ffmpeg_executable_path)

    # create the ffmpeg command
    """
    ffmpeg -i image.jpg -i audio.mp3 out.mp3 
    """

    ffmpeg_command = f"-i {image_to_convert_Path} -i {mp3_to_convert_Path} {mp4_outfile_Path}"
    cmd_command = f"{ffmpeg_executable_path} {ffmpeg_command}"


    print(f"input .mp3 file \n {mp3_to_convert_Path}")
    print()
    print(f"input image file \n {image_to_convert_Path}")
    print()
    print(f"output .mp4 file \n {mp4_outfile_Path}")
    print()
    print("cmd prompt command: ")
    print()
  

    # call ffmpeg
    returned_value = subprocess.call(cmd_command, shell=True)# returns the exit code in unix
    
    print("returned value:", returned_value)

if __name__ == "__main__":
      main()
