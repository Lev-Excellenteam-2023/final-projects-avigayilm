from PowerPointReader import read_powerpoint
import json

def main():
    ppName = 'End of course exercise - kickof - upload (1)'
    json_data= read_powerpoint(ppName)

    json_filename = "output.json"

    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)  # indent for pretty formatting

    print(f"JSON data saved as '{json_filename}'")


if __name__ == '__main__':
    main()

