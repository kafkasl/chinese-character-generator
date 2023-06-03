# Chinese Character Image Generator

This is a Python script for generating images of Chinese characters, along with their pronunciation (in Pinyin and Zhuyin), stroke order, and definition.

## Why?

Learning Chinese characters is an exciting journey and I wanted to make it a part of my everyday life. So, I came up with this project to transform my macOS desktop background into a dynamic learning tool. Now every day I have a new character, its stroke order, and meaning.

Each image features a Chinese character alongside its stroke order, depicted in shades of red, visually guiding you through the correct order and direction of each stroke. This is crucial for learning how to write Chinese characters correctly and can help improve your understanding and memory of each character's structure.

You can choose to generate images for characters from specific HSK levels, allowing you to start with simpler characters and gradually add more complex ones as your confidence grows. For example, you might start with only HSK level 1 characters, then progressively incorporate higher-level characters as your proficiency improves.

## Prerequisites

You'll need to have Python 3 and Go installed on your machine.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/chinese-character-generator.git
   cd chinese-character-generator
   ```

2. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Install `go-zhuyin`:

   ```shell
   go get github.com/shmokmt/go-zhuyin
   ```

## Usage

You can run the script with the following command:

```shell
python main.py
```

You can specify several command-line arguments:

- `--output-zhuyin`: Include Zhuyin in the output image (default: `True`).
- `--character-type`: The type of Chinese characters to use (choices: `traditional`, `simplified`; default: `traditional`).
- `--output-dir`: Directory to save the output images (default: `./images`).
- `--font`: Path to the font file to use (default: `NotoSansTC-Regular.otf`).
- `--input-file`: CSV file to read the Hanzi data from (default: `hanziDB.csv`).
- `--hsk-level`: HSK level for which characters should be generated (default: all levels).

## Acknowledgments

This project makes use of the following resources:

- Stroke order images are sourced from Wikimedia Commons.
- Hanzi data is sourced from [hanziDB](https://github.com/ruddfawcett/hanziDB.csv).
- Zhuyin conversion is performed using [go-zhuyin](https://github.com/shmokmt/go-zhuyin).

### Fonts

- The Noto fonts used in this project are from Google's [Noto Fonts](https://www.google.com/get/noto/) project, and are licensed under the SIL Open Font License.

## Contributing

We welcome contributions! Please feel free to submit a Pull Request or open an Issue.

## License

This project is licensed under MIT License - see the LICENSE file for details.
