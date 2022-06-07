from math import sqrt
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
import numpy

def solve_quadratic_equation(a, b, c):
    D = b**2 - 4*a*c
    if D < 0:
        return "No solutions"
    elif D == 0:
        return f"x = {-b/(2*a)}"
    else:
        x1 = (-b + sqrt(D))/(2*a)
        x2 = (-b - sqrt(D))/(2*a)
        return f"x1 = {x1}\nx2 = {x2}"

class QuadraticEquationView(View):
    def get(self, *args, **kwargs):
        data = self.request.GET
        a = data['a']
        b = data['b']
        c = data['c']
        result = solve_quadratic_equation(*[float(i) for i in [a,b,c]])
        return render(self.request, "result.html", {'result': result, 'quadratic': True})


class ColorGuesser(View):
    def get(self, *args, **kwargs):
        data = self.request.GET
        ordinal = data['ordinal']
        blue_prob = 0.6
        green_prob = 0.23
        red_prob = 0.17
        d = {'blue': blue_prob, 'green': green_prob, 'red': red_prob}
        if 'success' in data.keys():
            if data['success'] == 'True':
                result = data['result']
                context = {'text': f"Okay, so the result is {result}", 'result': result, 'success': True, 'quadratic': False, 'ordinal': ordinal}
                return render(self.request, "result.html", context=context)
        if 'first_not' in data.keys():
            first_not = data['first_not']
            if 'second_not' in data.keys():
                second_not = data['second_not']
                result = [x for x in ['red', 'green', 'blue'] if x not in [first_not, second_not]][0]
                context = {'text': f"Result is definitely {result}", 'result': result, 'success': True, 'quadratic': False, 'ordinal': ordinal}
                return render(self.request, "result.html", context=context)
            else:
                d.pop(first_not, None)
                next_list = [x for x in list(d.keys())]
                first_prob = d[next_list[0]]/(d[next_list[0]] + d[next_list[1]])
                second_prob = 1 - first_prob
                choice = numpy.random.choice(numpy.arange(1, 3), p=[first_prob, second_prob])
                context = {'text': f"Is it {next_list[choice -1]} then?", 'result': next_list[choice - 1], 'first_not': first_not, 'quadratic': False, 'ordinal': ordinal, 'success': False}
                return render(self.request, "result.html", context=context)
        else:
            choice = numpy.random.choice(numpy.arange(1, 4), p=[blue_prob, green_prob, red_prob])
            if choice == 1:
                result = "blue"
            elif choice == 2:
                result = "green"
            else:
                result = "red"
            return render(self.request, "result.html", {'text': f"Result is probably {result}", 'result': result, 'quadratic': False, 'ordinal': ordinal, 'success': False})
        
        

            