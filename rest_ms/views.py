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
        fin_ord = []
        quantities = []
        for i in order.order:
            quant = form[f'quant{i}']
            quantities.append(form[f'quant{i}'])
            if quant=='':
                fin_ord.append(i)
            else:
                for j in range(int(quant)):
                    fin_ord.append(i)
        order.order = fin_ord
        print(quantities)
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
        m=Menu.objects.all()
        # print(curr_table)
        if t:
            curr_table = t[len(t)-1]
            print(curr_table.order)
            items = curr_table.order
            uniques = []
            its = ''
            for ele in items:
                if ele.isdigit() or ele==',':
                    its += ele
            items = its.split(',')
            for item in items:
                if int(item) not in uniques:
                    print(item)
                    uniques.append(int(item))
            quant = []
            # print(uniques)
            for item in m:
                if item.id not in uniques:
                    uniques.append(item.id)
            # print(uniques)
            for item in uniques:
                quant.append(items.count(str(item)))
            # print(items)
            fin_order = []
            for item in uniques:
                fin_order.append(Menu.objects.get(id=int(item)))
            zipped = zip(fin_order,quant)
            context = {'table': curr_table, 'zipped': zipped}
            return render(request,'delete.html',context)
    messages.add_message(request, messages.INFO, f'Incorrect Table Number')
    
    return redirect('/')

def deleteitems(request,id):
    if request.method=='POST':
        form = request.POST
        print(id)
        t = Orders.objects.filter(table=id)
        curr_table = t[len(t)-1]
        uniques = []
        items = curr_table.order
        its = ''
        for ele in items:
            if ele.isdigit() or ele==',':
                its += ele
        items = its.split(',')
        for item in items:
            if item not in uniques:
                uniques.append(item)
        quant = []
        for item in uniques:
            quant.append(items.count(item))
        del_items = form.getlist('items')
        quantities=[]
        fin_ord=[]
        for i in del_items:
            q = form[f'quant{i}']
            quantities.append(form[f'quant{i}'])
            if q!='':
                for j in range(int(q)):
                    fin_ord.append(i)
        curr_table.order = fin_ord
        total = 0
        # if del_items != []:
        #     total = total - 0.18*total
        # for item in del_items:
        #     items.remove(item)
        #     it = Menu.objects.get(id=int(item))
        #     total -= float(it.price)
        #     total = round(total,2)
        for item in fin_ord:
            i = Menu.objects.get(id=int(item))
            total+=float(i.price)
        total = 1.18*total
        # curr_table.order = items
        curr_table.total=total
        curr_table.save()
        messages.add_message(request, messages.INFO, f'Order Edited Successfully')
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

# def ad(request):
#     if request.method=='POST':
#         form = request.POST
#         table = form['table']
#         menu = Menu.objects.all()
#         t = Orders.objects.filter(table=table)

#         if t:
#             curr_table = t[len(t)-1]
#             context = {'table': curr_table, 'menu':menu}
#             return render(request,'add.html',context)
#     messages.add_message(request, messages.INFO, f'Incorrect Table Number')
#     return redirect('/')

# def adtable(request,id):
#     if request.method=='POST':
#         form = request.POST
#         print(id)
#         t = Orders.objects.filter(table=id)
#         curr_table = t[len(t)-1]
#         old_order = curr_table.order
#         its = ''
#         for ele in old_order:
#             if ele.isdigit() or ele==',':
#                 its += ele
#         old_order = its.split(',')
#         new_order = form.getlist('add')
#         fin_ord = []
#         quantities = []
#         for i in new_order:
#             quant = form[f'quant{i}']
#             quantities.append(form[f'quant{i}'])
#             if quant == '':
#                 fin_ord.append(i)
#             else:
#                 for j in range(int(quant)):
#                     fin_ord.append(i)
#         print(fin_ord)
#         new_order = fin_ord
        
#         # curr_table.feedback = form['feed']
#         # curr_table.feedback_comments = form['comments']
#         if new_order != []:
#             for item in new_order:
#                 i = Menu.objects.get(id=item)
#                 curr_table.total += float(i.price)
#                 old_order.append(item)
#             curr_table.order = old_order
#             curr_table.total = 1.18*curr_table.total
#             curr_table.save()

#             messages.add_message(request, messages.INFO, f'More food is on its way')
#         else:
#             messages.add_message(request, messages.INFO, f'Incorrect Input')
#     return redirect('/')

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
    


