import json , glob, os

questions = ['nick-name', 'name', 'surename', 'telephone', 'e-mail', 'reason']
countquestions = len(questions)
tables = 20

def admin_menu() :
    global avil_tables
    avil_tables = 0
    while True :
        message = f'''
\\ ADMIN _ MENU //
         . 
1. set avilable tables today ({avil_tables} / {tables})
2. change menu list
3. add member 
         .
Enter choice : '''
        try:
            choice = input(message)
            match choice:
                case '1' : 
                    avil_tables = set_tables()
                case '2' :
                    admin_writemenu()
                case '3' :
                    add_member()
        except KeyboardInterrupt : return print('\n\n-----go back-----\n')
def set_tables() :
    while True :
        try : 
            avil = int(input(f'max tables is {tables} Enter avilable tables today (empty to exit ): '))
            if int(avil) <= tables and int(avil) >= 0: return(avil)
            else: print(f'we have tables {tables} place. set it equal or less than {tables} and not less than 0')
        except ValueError : print('Enter only number')

def admin_writemenu():
    while True:
        collect = []
        try:
            menu = int(input('Enter amount of menu you want to list (CTRL + C TO CANCEL ): '))
            for i in range(1,menu+1) : 
                name = input(f'Enter Name of Menu {i} : ')
                price = input(f'Enter Price of Menu {name} : ')
                detail = {
                    'no' : i,
                    'name' : name,
                    'price' : price
                }
                collect.append(detail)
        except KeyboardInterrupt : print('\n\ncancel write menu...\n\n'); break
        verify = input('Are you sure to replace Menu? (enter to success , type any key and enter to cancel) : ')
        if verify == '':
            with open('admin/database/data.json' , 'w' , encoding='utf-8') as send:
                json.dump(collect, send , ensure_ascii=False , indent=4)
            print('successfuly to replace menu')
            gen_customer_menu_list()
            break
        else :
            print('cancelled')

def gen_customer_menu_list():
    order = '''name : 
no. of table : 
List your menu that you want '''
    with open('admin/database/data.json' , 'r' , encoding='utf-8') as recive:
        data = json.load(recive)
    message = f'| {'NO.'.center(15)} - {'MENU'.center(15)} - {'PRICE'.center(15)} |\n'
    no = 1
    for i in data:
        message += f'| {str(no).center(15)} - {str(i['name']).center(15)} - {str(i['price']).center(15)} |\n'
        no += 1
    message += f'| {'ENJOY EATING'.center(51)} |\n'
    message += 'write order in order.txt by member number \nand sign "|" then write quantity.\n**important**\nEnter one line per one order.\nany unknown menu will be ignore.'
    with open('customer/LIST OF MENU.txt' , 'w') as f:
        f.write(message)
    with open('admin/report/LIST OF MENU.txt' , 'w') as f:
        f.write(message)
    with open('customer/order.txt' , 'w') as f:
        f.write(order)

def add_member():
    n = []
    while True:
        try :
            with open('admin/database/customer.json' , 'r' , encoding='utf-8') as recive:
                data = json.load(recive)
                break
        except FileNotFoundError : 
            with open('admin/database/customer.json' , 'w' , encoding='utf-8') as once:
                json.dump([] , once , ensure_ascii=False, indent=4)
    message = '''
    // REGISTER CUSTOMER \\
        Term of service.
    This is the project of
    COMPUTER-PROGRAMING
    Pls fill all of question
    below this description
    \\ Thankyou  customer //
    '''
    print(message)
    try:
        while True:
            detail = {}
            for q in questions:
                while True:
                    answer = input(f"{q}: ")
                    if q in [questions[0],questions[1],questions[2]]:
                        if not answer.isalpha():
                            print(f"{q} ต้องเป็นตัวอักษรเท่านั้น")
                            continue
                    elif q == questions[3]:
                        if not answer.isdigit() or len(answer) != 10:
                            print("เบอร์โทรศัพท์ต้องเป็นตัวเลข 10 หลัก")
                            continue
                    elif q == questions[4]:
                        if '@gmail.com' not in answer:
                            print("อีเมลต้องลงท้ายด้วย '@gmail.com'")
                            continue
                    detail[q] = answer
                    break  
            try:
                for i in data : n.append(i['number'])
                detail['number'] = max(n)+1
            except ValueError : detail['number'] = 1001
            data.append(detail)
            more = input("Do you want to add another member? (Enter to exit, any key to continue): ")
            if more == "":
                break
    except KeyboardInterrupt : print('\n\ncancel add member...\n\n')
    with open("admin/database/customer.json","w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    gen_member_report()
    print("Successfully added new members.")

def gen_member_report():
    message = ''
    with open('admin/database/customer.json' , 'r' , encoding='utf-8') as recive:
        data = json.load(recive)
    for i in questions :
        message += f'| {i.center(15)} '
        if i == questions[countquestions - 1]:
            message += f'| {'number'.center(15)}'
            message += '|\n'
    message += f'{'=' * len(message)}\n'
    for i in data :
        for q in questions :
            message += f'| {str(i[q]).center(15)} '
            if q == questions[countquestions - 1] :
                message += f'| {str(i['number']).center(15)}'
                message += '|\n'
    with open('admin/report/member_report.txt' , 'w' , encoding='utf-8') as report:
        report.write(message)

def recive_order():
    status = 'a+'
    order = {}
    menu = menu_order = []
    with open('customer/order.txt' , 'r' , encoding='utf-8') as recive:
        data = (recive.read()).splitlines()
    with open('admin/database/data.json' , 'r' , encoding='utf-8') as recive:
        data_menu = json.load(recive)
        for i in data_menu:
            i = list(i.values())[1]
            menu.append(i.lower())
    for s , d in enumerate(data , start = 1):
        try:
            value = d.split(' : ')
            order[value[0]] = value[1]
            if s == 2 and int(value[1].strip()) > tables: 
                message = f'sorry we have only {tables} tables'
                break
        except IndexError: pass
        try:
            value = d.split('|')
            value[1] = int(value[1].strip())
            if s > 3 and (value[1] != 0) and (' ' not in value[0].strip()) and (value[0].strip().lower() in menu) : 
                order[value[0].strip().lower()] = value[1]
                message = 'we already got your order'
        except IndexError: continue
        except TypeError: 
            message = 'enter only number after "|"'
            break
    menu_order.append
    try :
        with open(f'admin/database/table/tb_{order['no. of table']}_history.json' , 'r' , encoding='utf-8') as f:
            upd_order = json.load(f)
            upd_order.append(order)
        with open(f'admin/database/table/tb_{order['no. of table']}_history.json' , 'w' , encoding='utf-8') as f:
            json.dump(upd_order , f , ensure_ascii=False , indent=4)
    except FileNotFoundError :
        with open(f'admin/database/table/tb_{order['no. of table']}_history.json' , 'w' , encoding='utf-8') as f:
            json.dump([order] , f , ensure_ascii=False , indent=4)

    try:
        with open(f'admin/report/table/{order['no. of table']}_tb_order_report.txt' , status , encoding='utf-8') as report:
            report.write(f'{'-'*(41)}\n| {'MENU'.center(17)} | {'QUANTITY'.center(17)} |\n{'-'*(41)}\n')
            for t , i in enumerate(order ,start=1):
                if t > 2 : report.write(f'| {str(i).center(17)} | {str(order[i]).center(17)} |\n')
            report.write(f'{"="*14} END OF ORDER {"="*13}\n\n\n')
            clear_order(order['name'],order['no. of table'])
    except FileNotFoundError : status = 'w'
    try:
        return print(f'\n\n{message}\n\n')
    except UnboundLocalError : return print('\n\npls enter menu that you want.\n\n')

def clear_order(name,no):
    with open('customer/order.txt' , 'w' , encoding='utf-8') as f:
        f.write(f'name : {name}\nno. of table : {no}\nList your menu that you want ')

def bill():
    while True:
        menu = []
        detail = {}
        total = {}
        all = bill_total = 0
        while True:
            try :
                with open('admin/database/member_discounts.json' , 'r' , encoding='utf-8') as ds:
                    member_discounts = json.load(ds)
                    discount_lookup = {d['name']: d['discount'] for d in member_discounts}
            except (FileNotFoundError, json.JSONDecodeError):
                discount_lookup = {}
            try:
                table = int(input('Enter table number to print bill (ctrl + C to go back): '))
                if table > 0 and table <= tables : break
                else: print(f'we have only {tables} tables')
            except ValueError:
                print('Enter only number')
                continue
            except KeyboardInterrupt : return print('\n\n-----go back-----\n')
        try :
            with open(f'admin/database/table/tb_{table}_history.json' , 'r' , encoding='utf-8') as f:
                    total_order = json.load(f)
                    print(len(total_order))
        except FileNotFoundError : 
            print('This table is not have order')
            continue
        with open('admin/database/data.json' , 'r' , encoding='utf-8') as recive:
            data_menu = json.load(recive)
            for i in data_menu:
                i = list(i.values())[1]
                menu.append(i.lower())
        message = f'''{f'---- BILL OF TABLE {table} ----'.center(45)}   
        
{f'Customer name.. : {total_order[0]['name']}'.center(45)}

{'='*45}\n| {'MENU'.center(17)} | {'QUANTITY'.center(9)} | {'TOTAL(B.)'.center(9)} |\n{'='*45}\n|{' '*43}|\n'''
        for i in total_order :
            for d in list(i.keys()) :
                try:
                    if d in menu :
                        all = detail[d]
                        all += i[d]
                        detail[d] = all
                except KeyError : detail[d] = i[d]
        for s in data_menu:
            for r in list(detail.keys()) :
                if r in s['name'].lower():
                    total[f'{r}_total'] = detail[r]*float(s['price'])
        for x in detail:
            message += f'| {str(x).center(17)} | {str(detail[x]).center(9)} | {f'{total[f'{x}_total']:,.2f}'.center(9)} |\n|{' '*43}|\n'
            bill_total += total[f'{x}_total']
        try :
            discount = discount_lookup[total_order[0]['name']]
        except : discount = 0
        message += f'{'='*45}\n>>{'DISCOUNT'.center(29)}<< {f'{discount:,.2f}'.center(9)} |\n{'='*45}\n'
        message += f'{'='*45}\n>>{'TOTAL'.center(29)}<< {f'{bill_total-(bill_total*(discount/100)):,.2f}'.center(9)} |\n{'='*45}\n'
        with open(f'admin/report/bill/table_{table}_bill.txt' , 'w' , encoding='utf-8') as bill:
            bill.write(message)
        print(message)
        try:
            check = input('\npress Enter to end table(CTRL + C to cancel)\n')
            add_history(detail)
            member_point(table)
            calculate_member_discount()
            clear_table(table)
        except KeyboardInterrupt :
            try:
                print('\ncancel\n')
                out = input('enter to bill another(CTRL + C to main menu)\n')
                print('another check bill')
            except KeyboardInterrupt : return print('\n\n-----go back-----\n')

def clear_table(table) :
    os.remove(f'admin/report/bill/table_{table}_bill.txt')
    os.remove(f'admin/database/table/tb_{table}_history.json')
    os.remove(f'admin/report/table/{table}_tb_order_report.txt')
    print('\nsuccessfuly billed\n')

def add_history(detail) :
    while True:
        try:
            with open('admin/database/history.json' , 'r' , encoding='utf-8') as r :
                upd_datail = json.load(r)
                upd_datail.append(detail)
            with open('admin/database/history.json' , 'w' , encoding='utf-8') as history :
                json.dump(upd_datail, history , ensure_ascii=False , indent=4)
            break
        except FileNotFoundError :
            with open('admin/database/history.json' , 'w' , encoding='utf-8') as history :
                json.dump([], history , ensure_ascii=False , indent=4)

def daily_report():
    detail = {}
    total = {}
    menu = []
    all = bill_total = 0
    with open('admin/database/history.json' , 'r' , encoding='utf-8') as r :
        data = json.load(r)
    with open('admin/database/data.json' , 'r' , encoding='utf-8') as recive:
            data_menu = json.load(recive)
            for i in data_menu:
                i = list(i.values())[1]
                menu.append(i.lower())
    for i in data :
            for d in list(i.keys()) :
                try:
                        all = detail[d]
                        all += i[d]
                        detail[d] = all
                except KeyError : detail[d] = i[d]
    for s in data_menu:
            for r in list(detail.keys()) :
                if r in s['name'].lower():
                    total[f'{r}_total'] = detail[r]*float(s['price'])
    report = f'''\n\n{'--DaiLy Report--'.center(50)}

{'='*50}\n| {'MENU'.center(17)} | {'QUANTITY'.center(11)} | {'TOTAL(B.)'.center(12)} |\n{'='*50}\n|{' '*48}|\n'''
    for x in detail:
        report += f'| {str(x).center(17)} | {str(detail[x]).center(11)} | {f'{total[f'{x}_total']:,.2f}'.center(12)} |\n|{' '*48}|\n'
        bill_total += total[f'{x}_total']
    report += f'{'='*50}\n>>{'TOTAL'.center(31)}<< {f'{bill_total:,.2f}'.center(12)} |\n{'='*50}\n'
    with open('admin/report/daily_report.txt' , 'w' , encoding='utf-8') as daily :
        daily.write(report)
    print(report)

def member_point(table=None):

    point_file = 'admin/database/member_point.json'
    table_folder_pattern = f'admin/database/table/tb_{table}_history.json'

    # โหลดข้อมูลคะแนนเดิม (ถ้ามี) แล้วสร้าง dict เพื่อ merge โดยใช้ name เป็น key
    try:
        with open(point_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    points = {}
    for p in existing:
        key = str(p.get('name') or p.get('number') or '')
        if not key:
            continue
        points[key] = dict(p)
        points[key].setdefault('name', key)

    # อ่านทุกไฟล์ประวัติตารางและรวมยอด
    for filepath in glob.glob(table_folder_pattern):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tb = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            continue

        # tb คาดว่าเป็น list ของ dict แต่ละ dict คือตอนที่ลูกค้าสั่ง
        for order in tb:
            name = str(order.get('name') or order.get('number') or '').strip()
            if not name:
                continue

            if name not in points:
                points[name] = {'name': name}

            # รวมค่าแต่ละเมนู (ข้ามฟิลด์ที่ไม่ใช่เมนู เช่น 'name', 'time', 'date')
            for k, v in order.items():
                if k in ('name', 'number', 'time', 'date', 'no. of table'):
                    continue
                try:
                    qty = int(v)
                except (TypeError, ValueError):
                    # ถ้าค่าไม่ใช่จำนวนข้าม
                    continue
                points[name][k] = points[name].get(k, 0) + qty

    # บันทึกผลลัพธ์กลับเป็น list ของ dict ตามรูปแบบที่ต้องการ
    result = list(points.values())
    os.makedirs(os.path.dirname(point_file), exist_ok=True)
    with open(point_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    return result

def calculate_member_discount():
    DISCOUNT_RATES = {
        100: 5,    # สั่งครบ 100 ชิ้น ได้ส่วนลด 5%
        500: 10,   # สั่งครบ 500 ชิ้น ได้ส่วนลด 10%
        1000: 15,  # สั่งครบ 1000 ชิ้น ได้ส่วนลด 15%
        2000: 20   # สั่งครบ 2000 ชิ้น ได้ส่วนลด 20%
    }

    try:
        with open('admin/database/member_point.json', 'r', encoding='utf-8') as f:
            member_points = json.load(f)
        discounts = []
        for member in member_points:
            total_items = 0
            member_number = member.get('name', '')
            
            # รวมจำนวนอาหารทั้งหมด (ไม่นับ fields พิเศษ)
            for key, value in member.items():
                if key not in ['number', 'name', 'time', 'date']:
                    try:
                        total_items += int(value)
                    except (ValueError, TypeError):
                        continue
            
            # คำนวณส่วนลดตามจำนวนรวม
            discount = 0
            for threshold, rate in sorted(DISCOUNT_RATES.items()):
                if total_items >= threshold:
                    discount = rate
                else:
                    break
            
            # เก็บผลลัพธ์
            discounts.append({
                'name': member_number,
                'discount': discount
            })
        
        # บันทึกผลการคำนวณส่วนลด
        with open('admin/database/member_discounts.json', 'w', encoding='utf-8') as f:
            json.dump(discounts, f, ensure_ascii=False, indent=4)
        
        return discounts

    except FileNotFoundError:
        print("Error: member_point.json not found")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in member_point.json")
        return []
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def read_member_report():
    with open('admin/report/member_report.txt' , 'r' , encoding='utf-8') as report:
        rp = report.read()
    print(f'\n\n\n{rp}\n\n\n')

def report():
    message = '\n\nReport menu.\n1. daily report\n2.member report\n(CTRL + C to go back..)\n\nEnter menu : '
    try:
        while True:
            choice = input(message)
            if choice == '1' : daily_report()
            elif choice == '2' : read_member_report()
            else : print('no choice')
    except KeyboardInterrupt : return print('\n\n-----go back-----\n')
            
