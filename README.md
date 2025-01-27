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
# Company PF Details Manager

A Django-based web application for managing and tracking company Provident Fund (PF) details and payment information.

## Features

- Search and retrieve company PF details
- Automated data scraping from EPFS portal
- Store and display company information
- Track payment details including TRRN, credit dates, and employee counts
- Export data to Excel/CSV formats
- Interactive data tables with sorting and filtering capabilities

## Prerequisites

- Python 3.x
- Django
- Selenium WebDriver
- Pandas
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/company-pf-details.git
cd company-pf-details
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

## Project Structure

```
├── CompanyList/          # Directory for downloaded company data
├── data/                 # Directory for processed data files
├── static/              # Static files (CSS, JS)
├── templates/           # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── show_table.html
│   └── payment_details.html
├── utils/               # Utility functions
│   ├── checker.py
│   ├── db_func.py
│   ├── forms.py
│   ├── scrapper.py
│   └── scrapper_final.py
└── main.py             # Main application file
```

## Usage

1. Start the development server:
```bash
python main.py
```

2. Open your web browser and navigate to `http://localhost:8004`

3. Use the search form to look up company details

4. Select companies from the table to fetch their payment details

5. View and manage payment information in the payment details section

## Models

### Company_Data
- establishment_id (Primary Key)
- establishment_name
- address
- office_name

### Payment_Detail
- company_name
- trrn
- date_of_credit
- amount
- wage_month
- no_of_employee
- ecr

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
