# 3 Words for E-mail

An application with a **Flask backend** and a ** Js Frontend ** that sends three words and an image showing a forecast to the indicated email. The tool takes in two inputs and one image:

1. An e-mail address
2. Three words
3. An image among the 4 images

The user should write the message based on the sample text below the input box where the words will be entered.

## Setup

### Backend (Flask)
1. **Clone the Repository**:
   ```
   git clone https://github.com/poujoux/3wordsforemail.git
   cd watermark
   ```

2. **Set Up a Virtual Environment and Install Dependencies**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Flask Server**:
   ```
   flask run
   ```

### Frontend (JavaScript)
1. **Open index.html in your browser or type ```http://localhost:5000``` in the address bar of your browser.**
2. **The frontend will communicate with the Flask backend to send the mail.**


### .env File

1. **Get an AWS Access and an AWS Secret Access Key. How to obtain them:**
```https://docs.aws.amazon.com/IAM/latest/UserGuide/access-key-self-managed.html```

2. **Place your *AWS Access Key ID* and *AWS Secret Access Key* next to the *equal sign*. There is no need for bracketing/double quoting the keys or leaving a gap.**


## Usage

1. **Write the email**
    - Write the email you want to send the words to and maybe an image in the first input box.

2. **Input the words**
    - Type three words regarding to the sample text below in the place where you will input the words (the second input box).

3. **Select an image (Preferred)**
    - You can select an image among the 4 images. Only one image can be sent in a single post.

4. **Submit and Send it**
    - After filling in the places, tap the *Send* button and wait for the confirmation request mail to be sent to the indicated e-mail address. Within 120 seconds you need to confirm the request. Once it is confirmed, the last 5 sent elements will be displayed.


## License
This project is licensed under the MIT License.


