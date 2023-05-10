

<h3 align="center">DripDues</h3>



<h2 align="center"> The purpose of this project is to essentially take the mundane out of billing your tenants & to calculate their drip dues at warp speed so you don't have to.

</h2>

## 🧐 About <a name = "about"></a>

Simple python script that calculates monthly water, garbage & utility charges & generates invoices for several apartment units, stacking 7 invoices per page in a PDF document.


## 🏁 Getting Started <a name = "getting_started"></a>


### Prerequisites

```
Python
```

### Installing


Clone this repository

```
git clone https://github.com/Isaacg94/DripDues.git
```

Navigate into the directory

```
cd DripDues
```

Install ReportLab

```
pip install reportlab
```

## 🎈 Usage <a name="usage"></a>
Add some data to the **`meter_readings.csv`** file in the outlined format.

### Run the script

Whilst in your project directory on your terminal, run the following command:
```
python water_bill.py
```
## 💰 Roses are red, diamonds are blue, pockets is green, a permanent hue

The generated PDF file of invoices will appear inside the DripDues directory titled: **`current_month,current_year`** Drip Dues.pdf
