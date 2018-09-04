from django.shortcuts import render
from .forms import NewUserForm
from django import forms
from django.contrib.auth import authenticate,login,logout
#from django.contrib.auth.models import User
from .models import Complaints,User,DepartmentAdmins_list,ComplaintAssignment,Comments
#from .models import Complaints
from django.contrib.auth.models import Permission
import os.path
import csv
import ast #ast module is used to convert string to dictionary format
# Create your views here.
filepath="C:\\Users\\NIKITHA\\Downloads\\DjangoApplication-new (2) (1)\\DjangoApplication1\\ProOne\\appOne\\userdetails.csv"
def index(request):
    return render(request,'appOne/index.html')
def employees(request):
    form=NewUserForm()
    if (request.method=='POST'):
        form=NewUserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("eroor form invalid")
    return render(request,'appOne/employees.html',{'form':form})
def signup(request):

    dic=request.POST
    print(dic)
    if len(dic)==0:
        return render(request,'appOne/signup.html')
    else:
        fieldnames = ['username', 'mobilenumber', 'emailid', 'address', 'department', 'employeeid', 'password',
                      'confirmpassword']


        if  not os.path.isfile(filepath):
            with open(filepath,'a+') as f:
                writer=csv.DictWriter(f,fieldnames)
                writer.writeheader()
                writer.writerow({'username':dic['username'],'mobilenumber':dic['mobilenumber'],'emailid':dic['emailid'],'address':dic['address'],'department':dic['department'],'employeeid':dic['employeeid'],
                'password':dic['password'],'confirmpassword':dic['confirmpassword']})
        else:
            with open(filepath,
                      'a+') as f:

                writer = csv.DictWriter(f,fieldnames)
                writer.writerow(
                    {'username': dic['username'], 'mobilenumber': dic['mobilenumber'], 'emailid': dic['emailid'],
                     'address': dic['address'], 'department': dic['department'], 'employeeid': dic['employeeid'],
                     'password': dic['password'], 'confirmpassword': dic['confirmpassword']})
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("nikitha.m363@gmail.com", "darling.dady")

        msg = "Hi \n new user created with name {0} ".format(dic['username'])

        server.sendmail("nikitha.m363@gmail.com", "nikkimachineni123@gmail.com", msg)

        server.quit()

        return index(request)
def loginconnection(request):
    dic=request.POST
    if not bool(dic):
        return render(request,'appOne/login.html')
    else:
        user_name=dic['username']
        pass_word=dic['password']
        #print(user_name,pass_word)
        user=User.objects.filter(username=user_name)
        try:
            valid_admin=DepartmentAdmins_list.objects.get(d_username=user_name)
        except Exception as e:
            valid_admin=None
       # print(user)
        if user:
            valid_user=authenticate(request,username=user_name,password=pass_word)
            #print(valid_user)

            if valid_user is not None:
               # print("hello")
                login(request,valid_user)
                open_count=len(Complaints.objects.filter(complaint_status="open"))
                unresolved_count=len(Complaints.objects.filter(complaint_status="InProgress"))
                close_count=len(Complaints.objects.filter(complaint_status="close"))
                return render(request,'appOne/helpdesk_portal.html',{'dic':dic,'valid_user':valid_user,'valid_admin':valid_admin,'open_count':open_count,'unresolved_count':unresolved_count,'close_count':close_count})
            else:
                return render(request,'appOne/login.html',{'loginfail':'INVALID CREDENTIALS'})
        else:
            return render(request,'appOne/login.html',{'invaliduser':'INVALID USER DETAILS'})
def logout_view(request):
    logout(request)
    return render(request,'appOne/login.html')

def activate(request,userDetails):
    #print("helooo here is Iam:", userDetails)
    #print(type(userDetails))
    dic=dict(request.POST)
    print(dic)

    if str(userDetails).startswith('{'):
        userDetails=ast.literal_eval(userDetails)
        #print(type(userDetails))
        print("user details are:",userDetails)
        print(request.POST)
        if  len(User.objects.all())==0:
            user = User.objects.create_superuser(username=userDetails['username'], email=userDetails['emailid'],
                                            password=userDetails['password'],
                                            mobilenumber=int(userDetails['mobilenumber']),
                                            department=userDetails['department'],
                                            employeeid=int(userDetails['employeeid']), address=userDetails['address'])
        else:
             #print(dic['depadmin'])
             if dic['depadmin']== "on":
                 user = User.objects.create_user(username=userDetails['username'], email=userDetails['emailid'],
                                                 password=userDetails['password'],
                                                 mobilenumber=int(userDetails['mobilenumber']),
                                                 department=userDetails['department'],
                                                 employeeid=int(userDetails['employeeid']),
                                                 address=userDetails['address'])
                 departmentadmin=DepartmentAdmins_list(
                     d_id=userDetails['employeeid'],
                     d_name=userDetails['department'],
                     d_username=userDetails['username']
                 )
                 departmentadmin.save()
                # permission = Permission.objects.get(name='request.POST')
                 #user.user_permissions.add(permission)

             else:

                  user=User.objects.create_user(username=userDetails['username'],email=userDetails['emailid'],password=userDetails['password'],mobilenumber=int(userDetails['mobilenumber']),department=userDetails['department'],employeeid=int(userDetails['employeeid']),address=userDetails['address'])
        print("user is:",user)
        user.is_staff=True
        user.save()
        if user is not None:
            import csv
            rows=[]
            with open(filepath ,'r') as csvfile:
                csvReader = csv.DictReader(csvfile)
                rows = [dict(row) for row in csvReader if row['username']!=userDetails['username']]
                # csvfile.truncate()
                print("rows are :",rows)
            csvfile.close()


            with open(filepath, 'w+') as csvfile:
                fieldnames = ['username', 'mobilenumber', 'emailid', 'address', 'department', 'employeeid', 'password',
                              'confirmpassword']
                csv_writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerows(rows)


            print("here Iam ------------")

            return render(request,'appOne/userdetails.html',{'msg':'user activated successfully','d':list(rows)})
        else:
            return render(request, 'appOne/userdetails.html',{'msg':"user not activated"})
    else:
        print()
        return render(request, 'appOne/login.html')


def pendingusers(request):
    import csv
    f = open(filepath, "r")
    reader = csv.DictReader(f)

    output = [dict(row) for row in reader]
    #print(output)
    return render(request,'appOne/userdetails.html',{'d':list(output)})
def forgotpassword(request):
    dic = request.POST
    if not bool(dic):
        return render(request, 'appOne/forgotpassword.html')

    if bool(request.POST):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("nikitha.m363@gmail.com", "darling.dady")

        msg = "Hi \n  Here is your link to change password http://127.0.0.1:8000/resetpassword/{0}".format(request.POST['emailid'])

        server.sendmail("nikitha.m363@gmail.com", request.POST["emailid"], msg)
        #print(request.POST["emailid"])
        server.quit()
    return render(request, 'appOne/login.html')

def changepassword(request,emailid):
    #dic=request.POST
   # print(emailid)

    return render(request, 'appOne/resetpassword.html',{'emailid':emailid})

def setpassword(request):
    dic=dict(request.POST)
    print("jioj",dic['emailid'])
    if not bool(dic):
        return render(request,'appOne/resetpassword.html')
    else:
        user=User.objects.get(email=str(dic['emailid'][0]))
        #user=User.objects.all()
        print(user)
        print(str(dic['newpassword'][0]))
        if str(dic['newpassword'][0])==str(dic['confirmnewpassword'][0]):
            user.set_password(str(dic['newpassword'][0]))
            user.save()
            return render(request,"appOne/login.html",{'msg':"Password updated Successfully"})
        else:
            return render(request,'appOne/resetpassword.html',{'emailid':str(dic['emailid'][0]),"msg":"Password mismatch"})

    #return render(request,'appOne/login.html',{"no match": "passwords didn't match"})

def RegisterComplaint(request):
    #print(request.POST)
    if request.user.is_authenticated:
        dic=request.POST
        print(dic)
        user=User.objects.get(username=str(request.user.username))
        print(user)
        print(user.email)
        complaint=Complaints(
            complaint_title=dic['complainttitle'],
            complaint_department=dic['department'],
            complaint_description=dic['description'],
            complaint_status='open',
            complaint_username=request.user.username,
            complaint_email=user.email,
            complaint_priority=dic['priority'],
        )
        complaint.save()
        #print(request.user.username)
        return render(request,'appOne/helpdesk_portal.html')

    else:
        print("invalid credentials")
def helpdesk(request):
    if request.user.is_authenticated:
        #print(request.user.username)
        valid_user = User.objects.get(username=str(request.user.username))#to create this object again
        #print(valid_user.is_superuser)
    if valid_user is not None:
        open_count = len(Complaints.objects.filter(complaint_status="open"))
        unresolved_count = len(Complaints.objects.filter(complaint_status="InProgress"))
        close_count = len(Complaints.objects.filter(complaint_status="close"))
        return render(request, 'appOne/helpdesk_portal.html',
                      { 'valid_user': valid_user,  'open_count': open_count,
                       'unresolved_count': unresolved_count, 'close_count': close_count})

    else:
        return render(request, 'appOne/helpdesk_portal.html')


def tickets(request):
    #user=User.objects.get(username=request.user.username)
    try:
        user=DepartmentAdmins_list.objects.get(d_username=request.user.username)
    except Exception as e:
        print(e)
        user=None

    #print(user)
    #print(user.department)
    #complaints=Complaints.objects.all()
    #print(complaints[1].complaint_department)
    #print(complaints[0].complaint_department)
    #print(Complaints.objects.filter(complaint_department=user.department))

   # print(complaint)
    #print(Complaints.objects.get(complaint_department=str('Networks')))
    #if user.department=='Networks':
        #tickets=Complaints.objects.get(complaint_department='Networks')
    #if user.department=='Human resources':
        #tickets=Complaints.objects.get(complaint_department='Human resources')
    #print(tickets)
    #print(tickets[2])
    #print(tickets[2].complaint_id)
    if user is not None:
        tickets = Complaints.objects.filter(complaint_department=user.d_name)
        print(tickets)

        admins= DepartmentAdmins_list.objects.filter(d_name=user.d_name)
        print(admins)
        #for i in admins:
            #print(i.d_name)
        return render(request,'appOne/tickets.html',{'tickets':list(tickets),'admins':admins})
    else:
        tickets=Complaints.objects.all()
        return render(request, 'appOne/tickets.html', {'tickets': tickets})
def mytickets(request):
    mytickets=[]

    if(request.user.is_authenticated):
        #tickets = Complaints.objects.all()
        #for i in tickets:
           # if request.user.username==i.complaint_username:
               # mytickets.append(i)
        #print(request.user.username)
        mytickets=Complaints.objects.filter(complaint_username=request.user.username)
        #print(mytickets)
        return render(request,'appOne/mytickets.html',{'mytickets':mytickets})
def assignment(request,complaintDetails):
    print(request.POST)
    print(request.POST['assigned'])
    complaint=Complaints.objects.get(complaint_id=complaintDetails)
    print(complaint)
    #print(type(complaint))
    complaint.complaint_status='InProgress'
    #assigned=request.POST['assigned']
    complaint.save()

    comp_assign=ComplaintAssignment(
         comp_id=complaint.complaint_id,
         dep_name=complaint.complaint_department,
         complaint_assignment=request.POST['assigned'],
     )
    comp_assign.save()
    return render(request,'appOne/helpdesk_portal.html')
def assignedtickets(request):
    assigned=ComplaintAssignment.objects.filter(complaint_assignment=request.user.username)
    assigned_tickets=[]
    for i in assigned:
        complaint = Complaints.objects.get(complaint_id=i.comp_id)
        if complaint is not None:
            assigned_tickets.append(complaint)

    #print(assigned_tickets)
    return render(request,'appOne/assignedtickets.html',{'assigned_tickets':assigned_tickets})
def comments(request,complainttitle):
    print("entered comments view")
    comments = Comments.objects.filter(complaint_name=complainttitle)
    return render(request,'appOne/comments.html',{'comments':comments,'complainttitle':complainttitle})
def Addcomment(request,complainttitle):
    print("hello")
    comments=Comments.objects.filter(complaint_name=complainttitle)
    return render(request,'appOne/Addcomment.html',{'comments':comments,'complainttitle':complainttitle})
def savecomment(request,complainttitle):
    print(request.POST)
    dic=request.POST
    comment_detail=Comments(
        complaint_name=complainttitle,
        response_no=dic['response_no'],
        comment=dic['comment'],
    )
    comment_detail.save()
    comments=Comments.objects.filter(complaint_name=complainttitle)
    return render(request,'appOne/comments.html',{'comments':comments,'complainttitle':complainttitle})
def close(request,complaintid):
    print(complaintid)
    complaint1=Complaints.objects.get(complaint_id=complaintid)
    print(complaint1)
    complaint1.complaint_status="close"
    print(complaint1.complaint_status)
    complaint1.save()
    assigned = ComplaintAssignment.objects.filter(complaint_assignment=request.user.username)
    assigned_tickets = []
    for i in assigned:
        complaint = Complaints.objects.get(complaint_id=i.comp_id)
        if complaint is not None:
            assigned_tickets.append(complaint)

    return render(request,'appone/assignedtickets.html',{'assigned_tickets':assigned_tickets})
def close1(request,complaintid):
    print(complaintid)
    complaint1=Complaints.objects.get(complaint_id=complaintid)
    print(complaint1)
    complaint1.complaint_status="close"
    print(complaint1.complaint_status)
    complaint1.save()
    if (request.user.is_authenticated):
        mytickets = Complaints.objects.filter(complaint_username=request.user.username)
        # print(mytickets)
        return render(request, 'appOne/mytickets.html', {'mytickets': mytickets})
