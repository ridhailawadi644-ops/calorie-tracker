from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)
CSV_FILE = "meals.csv"


def load_meals():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df.to_dict(orient="records")
        except pd.errors.EmptyDataError:
            return []
    return []


def save_meals(meals):
    if meals:
        df = pd.DataFrame(meals)
    else:
        df = pd.DataFrame(columns=["name", "calories", "protein"])
    df.to_csv(CSV_FILE, index=False)


@app.route("/", methods=["GET", "POST"])
def index():
    meals = load_meals()

    if request.method == "POST":
        name = request.form["name"]
        calories = int(request.form["calories"])
        protein = int(request.form["protein"])

        meals.append({
            "name": name,
            "calories": calories,
            "protein": protein
        })

        save_meals(meals)
        return redirect("/")

    total_calories = sum(m["calories"] for m in meals)
    total_protein = sum(m["protein"] for m in meals)

    return render_template("index.html",
                           meals=meals,
                           total_calories=total_calories,
                           total_protein=total_protein)


# ✅ DELETE ROUTE
@app.route("/delete/<int:index>")
def delete(index):
    meals = load_meals()

    if 0 <= index < len(meals):
        meals.pop(index)
        save_meals(meals)

    return redirect("/")


# ✅ RESET ROUTE
@app.route("/reset")
def reset():
    save_meals([])
    return redirect("/")


if __name__ == "__main__":
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    meals = load_meals()

    if index < 0 or index >= len(meals):
        return redirect("/")

    if request.method == "POST":
        meals[index]["name"] = request.form["name"]
        meals[index]["calories"] = int(request.form["calories"])
        meals[index]["protein"] = int(request.form["protein"])

        save_meals(meals)
        return redirect("/")

    meal = meals[index]
    return render_template("edit.html", meal=meal, index=index)