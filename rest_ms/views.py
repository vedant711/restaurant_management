from django.shortcuts import render,redirect
from .models import Orders, Menu
from django.contrib import messages

# messages.add_message(request, messages.INFO, 'Incorrect Input')

# Create your views here.
def index(request):
    menu =  Menu.objects.all()
    order = Orders.objects.all()
    context = {'menu': menu, 'orders':order}
    return render(request, 'index.html', context)

def add(request):
    if request.method == 'POST':
        form = request.POST
        order=Orders()
        order.order = form.getlist('items')
        print(form.getlist('items'))
        order.table = form['table']
        total = 0
        for item in order.order:
            it = Menu.objects.get(id=int(item))
            total += it.price
        order.total = round(1.18*total,2)
        order.feedback = ''
        order.feedback_comments = ''
        if order.order != [] and order.table!=0:
            order.save()
            messages.add_message(request, messages.INFO, f'Food is on its Way')
        else:
            messages.add_message(request, messages.INFO, f'Incorrect Input')
    return redirect('/')

def delete(request):
    if request.method=='POST':
        form = request.POST
        table = form['table']
        t = Orders.objects.filter(table=table)
        # print(curr_table)
        if t:
            curr_table = t[len(t)-1]
            print(curr_table.order)
            items = curr_table.order
            its = ''
            for ele in items:
                if ele.isdigit() or ele==',':
                    its += ele
            items = its.split(',')
            print(items)
            fin_order = []
            for item in items:
                fin_order.append(Menu.objects.get(id=int(item)))
            context = {'table': curr_table, 'order':fin_order}
            return render(request,'delete.html',context)
    messages.add_message(request, messages.INFO, f'Incorrect Table Number')
    
    return redirect('/')

def deleteitems(request,id):
    if request.method=='POST':
        form = request.POST
        print(id)
        t = Orders.objects.filter(table=id)
        curr_table = t[len(t)-1]
        items = curr_table.order
        its = ''
        for ele in items:
            if ele.isdigit() or ele==',':
                its += ele
        items = its.split(',')
        del_items = form.getlist('items')
        total = curr_table.total
        if del_items != []:
            total = total - 0.18*total
        for item in del_items:
            items.remove(item)
            it = Menu.objects.get(id=int(item))
            total -= float(it.price)
            total = round(total,2)
        curr_table.order = items
        curr_table.total=total
        curr_table.save()
        messages.add_message(request, messages.INFO, f'Items Removed Successfully')
        return redirect('/')

def feedback(request):
    if request.method=='POST':
        form = request.POST
        table = form['table']
        t = Orders.objects.filter(table=table)
        if t:
            curr_table = t[len(t)-1]
            context = {'table': curr_table}
            return render(request,'feedback.html',context)
    messages.add_message(request, messages.INFO, f'Incorrect Table Number')
    return redirect('/')

def feedtable(request,id):
    if request.method=='POST':
        form = request.POST
        print(id)
        t = Orders.objects.filter(table=id)
        curr_table = t[len(t)-1]
        curr_table.feedback = form['feed']
        curr_table.feedback_comments = form['comments']
        curr_table.save()
        if curr_table.feedback == 'bad' or curr_table.feedback == 'average':
            messages.add_message(request, messages.INFO, f'We will try to improve our Service')
        elif curr_table.feedback == 'good' or curr_table.feedback == 'excellent':
            messages.add_message(request, messages.INFO, f'We are delighted with your compliments')

        else:
            messages.add_message(request, messages.INFO, f'Unable to Save Feedback')
    return redirect('/')

def ad(request):
    if request.method=='POST':
        form = request.POST
        table = form['table']
        menu = Menu.objects.all()
        t = Orders.objects.filter(table=table)

        if t:
            curr_table = t[len(t)-1]
            context = {'table': curr_table, 'menu':menu}
            return render(request,'add.html',context)
    messages.add_message(request, messages.INFO, f'Incorrect Table Number')
    return redirect('/')

def adtable(request,id):
    if request.method=='POST':
        form = request.POST
        print(id)
        t = Orders.objects.filter(table=id)
        curr_table = t[len(t)-1]
        old_order = curr_table.order
        its = ''
        for ele in old_order:
            if ele.isdigit() or ele==',':
                its += ele
        old_order = its.split(',')
        new_order = form.getlist('add')
        for item in new_order:
            i = Menu.objects.get(id=item)
            curr_table.total += float(i.price)
            old_order.append(item)
        curr_table.order = old_order
        curr_table.total = 1.18*curr_table.total
        # curr_table.feedback = form['feed']
        # curr_table.feedback_comments = form['comments']
        curr_table.save()
        if new_order != []:
            messages.add_message(request, messages.INFO, f'More food is on its way')
        else:
            messages.add_message(request, messages.INFO, f'Incorrect Input')
    return redirect('/')

def bill(request):
    if request.method=='POST':
        form = request.POST
        table = form['table']
        t = Orders.objects.filter(table=table)
        if t:
            curr_table = t[len(t)-1]
            total = curr_table.total
            messages.add_message(request, messages.INFO, f'Your Total bill is ₹{total}')
        else:
            messages.add_message(request, messages.INFO, f'Incorrect Table Number')

    return redirect('/')
    


