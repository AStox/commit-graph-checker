# GitHub Commit Reminder

This Python script, `commitChecker.py`, sends a reminder email to you if no GitHub commits are found for the current day. It's a handy tool for developers who want to keep their GitHub commit graph green and need a little nudge to make daily commits.

## Installation

1. **Clone the Repository**: Clone this repository to your local machine using:

   ```
   git clone <repository_url>
   ```

2. **Set Up a Virtual Environment**: (Optional, but recommended) Create a virtual environment using:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Libraries**: Install the necessary Python libraries using:

   ```bash
   pip install smtplib requests PyGithub python-dotenv
   ```

4. **Configure Environment Variables**: Copy the `.env.example` file to a new file named `.env` and fill in your details.

## Usage

### Running the Script Manually

1. **Run the Script**: Execute the script using:

   ```bash
   python commitChecker.py
   ```

   The script will check your GitHub repositories for commits made today, and if none are found, it will send a reminder email to the specified email address.

### Running the Script as a Cron Job

1. **Open the Crontab**: Open your user's crontab file by running:

   ```bash
   crontab -e
   ```

2. **Add the Cron Job**: Add the following line to the crontab file to run the script every day at 8 PM:

   ```cron
   0 20 * * * /usr/bin/python /path/to/your/commitChecker.py
   ```

   Make sure to replace `/path/to/your` with the actual path to the `commitChecker.py` file, and update the Python path if needed.

3. **Save and Exit**: Save the crontab file and exit the editor. The new cron job will now run at the specified time.

## Customization

- **Add More Repositories**: By default, the script checks all repositories you have access to. Modify the `get_repos` function if you want to customize the repositories being checked.
- **Customize Email Content**: You can change the email subject and body in the `send_email_notification` function.

## Security Note

Make sure to keep your `.env` file secure, as it contains sensitive information such as email credentials and GitHub personal access tokens.

## Contributing

Feel free to fork this repository and submit pull requests. Any contributions are welcome!

## License

This project is open-source and available under the MIT License.
