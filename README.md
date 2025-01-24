Here's a comprehensive `README.md` file for your GitHub repository. It includes sections for project description, features, requirements, setup, and more.
# Company PF Details Management System

This project is a web application for managing company PF (Provident Fund) details. It allows users to search for company details, scrape data, store it in a database, and display payment details in an organized manner.

---

## Screenshots

### Homepage
![Homepage](https://github.com/user-attachments/assets/fd097891-141d-4e44-9858-972451d70b81)

---

### Search Page
![Search Page](https://github.com/user-attachments/assets/378dc18b-d4f0-4be8-b8d6-b36507ba6cb2)

---

### Company List
![Company List](https://github.com/user-attachments/assets/df4598f8-70f5-45c4-adab-ab4b438388e8)

---

### Table Display
![Table Display](https://github.com/user-attachments/assets/62c9663d-5d8a-47f0-a77f-639275d20d02)

---

### Company_name list
![Payment Details](https://github.com/user-attachments/assets/10dc3daa-7bf6-424c-8df3-e5732389f19c)

---

### Database Integration
![image](https://github.com/user-attachments/assets/669c818e-40c7-4468-955f-ffbecad3c788)
![image](https://github.com/user-attachments/assets/9aa8ba86-311b-4787-8ebb-068a4b3b296e)



---

### Scrapper_final
![CSV Processing](https://github.com/user-attachments/assets/eed30a8a-a3af-43ae-8a8c-cec8fe371cef)

---

### Scraper in Action
![Scraper](https://github.com/user-attachments/assets/4d743b63-9afe-4b56-9220-6a98e7db468a)

---

### Payment_details
![Error Handling](https://github.com/user-attachments/assets/e5e2957c-9f36-465b-8866-01d58b1ae4d3)







```markdown
# Company PF Details Management System

This project is a web application for managing company PF (Provident Fund) details. It allows users to search for company details, scrape data, store it in a database, and display payment details in an organized manner.

## Features

- **Search and Scrape**: Search for a company by name and scrape its PF-related data.
- **Database Integration**: Store and manage company details in a SQLite database.
- **Dynamic Table Display**: Display company data and payment details in a user-friendly table format.
- **Error Handling**: Handles errors during scraping and data processing gracefully.
- **Interactive UI**: Built with Django templates for dynamic rendering and user interaction.
- **CSV and Excel Handling**: Process and validate CSV/Excel files for data storage.

---

## Project Structure


```
📂 Project Root
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── CompanyList/        # Directory for downloaded files
├── data/               # Directory for processed data
├── db_func.py          # Database operations
├── scrapper.py         # Web scraping utilities
├── scrapper_final.py   # Finalized scraping logic
├── checker.py          # Excel validation utilities
├── views.py            # Django views
├── requirements.txt    # Python dependencies
└── app.py              # Entry point of the application
```

---


## Technologies Used

- **Backend**: Django, NanoDjango, SQLite
- **Frontend**: HTML, CSS, Django Templates
- **Web Scraping**: Selenium, pandas
- **Libraries**: 
  - `pandas` for data processing
  - `selenium` for scraping
  - `xlsx2csv` for Excel to CSV conversion

---

## Installation

### Prerequisites
1. Python 3.9+ installed on your system.
2. A modern web browser (e.g., Chrome).
3. ChromeDriver for Selenium (ensure it matches your Chrome version).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/company-pf-details.git
   cd company-pf-details
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up directories:
   ```bash
   mkdir CompanyList data
   ```

4. Run the application:
   ```bash
   python app.py
   ```
   The app will automatically open in your default browser at `http://localhost:8004`.

---

## Usage

1. Navigate to the homepage.
2. Enter the company name in the search bar and hit "Search."
3. View and select the desired company from the results table.
4. Scrape payment details for selected companies and view them on the payment details page.

---

## API Reference

### `/`
- **Method**: GET
- **Description**: Renders the homepage.

### `/search`
- **Method**: GET
- **Description**: Handles search requests, scrapes data, and stores it in the database.

### `/show_table`
- **Method**: GET, POST
- **Description**: Displays the table of company data. Accepts selections for further scraping.

### `/payment_details`
- **Method**: GET
- **Description**: Displays the payment details table.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Create a pull request.

---

## Troubleshooting

- **Selenium WebDriver Errors**:
  - Ensure `chromedriver` is in your `PATH`.
  - Update `chromedriver` to match your browser version.

- **Database Issues**:
  - Ensure `company_pf_details.db` is writable.
  - Check for missing tables in SQLite.

- **File Not Found Errors**:
  - Ensure directories (`CompanyList`, `data`) are created and accessible.


---

## Contact

For any issues or suggestions, feel free to reach out:

- **Author**: Vaibhav joshi
- **Email**: vashu941130@gmail.com
```
.
