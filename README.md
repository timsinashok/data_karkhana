# Data Karkhana

## Description

Data Karkhana is a project focused on building a Hybrid System for file sharing based on both Client Server model and P2P model. We have five components in the system: a tracker, 2 peers, a sender (Alice), and a receiver (Bob). Alice also acts as a peer after sending files to the system. Bob can receive the file but doesn't act as a peer in the system.

## Installation

To install and run this project, you would need to follow one of the following steps:

### 1) PyPI
The package is hosted in Pipy [here](https://pypi.org/project/datakarkhana/), you can directly download it using the command below:
```bash
pip install datakarkhana
```
Then you can directly run <b>datakarkhana</b> from your terminal.

### 2) Clone this repository
To install and run this project you would need to follow one of the following steps:

1. Clone the repo:
```bash
git clone https://github.com/timsinashok/data_karkhana.git
```

3. Navigate into the project directory:
cd data_karkhana, and run the main.py script. 

## Usage
If using Pipy use the following: 
```bash
datakarkhana {tracker ip} {tracker port}
```
If you are cloning this repository, use the following
```bash
python3 main.py {tracker ip} {tracker port}
```
, and continue with the instructions in the terminal.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
