from cdk8s import App

from charts.first import FirstChart
from charts.exercise import ExerciseChart 

app = App()
FirstChart(app, "tglanz-first-chart")
ExerciseChart(app, "tglanz-exercise-chart")

app.synth()

