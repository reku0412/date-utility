from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# ツェラーの公式による曜日計算
def zeller_congruence(day, month, year):
    if month < 3:
        month += 12
        year -= 1

    k = year // 100
    j = year % 100

    h = day + (26 * (month + 1) // 10) + 5 * k + (k // 4) + j + (j // 4)
    z = h % 7

    return z


# 曜日の表示
def show_day_of_week(z):
    days = ["土曜日", "日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日"]
    return days[z]

# 閏年判定
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# 年初からの日数計算
def day_of_year(year, month, day):
    date = datetime(year, month, day)
    start_of_year = datetime(year, 1, 1)
    return (date - start_of_year).days + 1

# 残り日数計算
def remaining_days(year, month, day):
    total_days = 366 if is_leap_year(year) else 365
    return total_days - day_of_year(year, month, day)

#生きてきた日数
def lived_days(birthday, target_date):
    return (target_date - birthday).days

#100歳までの何日あるか
def get_hundred_birthday(birthday):
    try:
        return birthday.replace(year=birthday.year + 100)
    except ValueError:
        # 2月29日生まれの場合、100年後は2月28日にする
        return birthday.replace(year=birthday.year + 100, day=28)
    
def days_until_hundred(birthday, target_date):
    hundred_birthday = get_hundred_birthday(birthday)
    return (hundred_birthday - target_date).days



@app.route("/", methods=["GET", "POST"])
def index():

    # 初期値
    year = None
    month = None
    day = None
    
    weekday = ""
    leap_text = ""
    day_number = None
    remaining = None
    result = ""

    lived = None
    remaining_to_hundred = None

    if request.method == "POST":

        try:
            date = request.form["date"]

            year, month, day = map(int, date.split("-"))

            # 日付チェック
            datetime(year, month, day)

            # 曜日
            z = zeller_congruence(day, month, year)
            weekday = show_day_of_week(z)

            # 閏年
            leap = is_leap_year(year)
            leap_text = "はい 🌏" if leap else "いいえ"

            # 年初からの日数
            day_number = day_of_year(year, month, day)

            # 年末まで
            remaining = remaining_days(year, month, day)

            # 生きてきた日数
            birthday = request.form["birthday"]
            target_date = request.form["target_date"]

            birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
            target_date = datetime.strptime(target_date, "%Y-%m-%d")

            lived = lived_days(birthday_date, target_date)
            remaining_to_hundred = days_until_hundred(birthday_date, target_date)

        except ValueError:
            result = "⚠️ 無効な日付です。"

    return render_template(
    "index.html",
    year=year,
    month=month,
    day=day,
    weekday=weekday,
    leap=leap_text,
    day_of_year=day_number,
    remaining_days=remaining,
    result=result,
)
if __name__ == "__main__":
    app.run(debug=True)