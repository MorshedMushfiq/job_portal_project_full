from django.shortcuts import  render,  redirect,   get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import  HttpResponse, Http404
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from App.models import *





# for register with validation
def register(req):
    if req.method=='POST':
        uname = req.POST.get('uname')
        fname = req.POST.get('first_name')
        lname = req.POST.get('last_name')
        city = req.POST.get('city')
        gender = req.POST.get('gender')
        profile_img = req.FILES.get('profile_img')
        email = req.POST.get('email')
        password = req.POST.get('password')
        user_type =  req.POST.get('user_type')
        confirm_password = req.POST.get('confirm_password')
        if not all([uname, email, user_type, password, confirm_password, fname, lname, city, gender, profile_img]):
            messages.error(req, 'Please fill all the fields')
            return render(req, 'common/register.html')
        try: 
            validate_email(email)
        except ValidationError:
            messages.error(req, 'Invalid email')
            return render(req, 'common/register.html')

        if password != confirm_password:
            messages.error(req,  "Password & Confirm Password Not Matched!")
            return render(req, 'common/register.html')
        if len(password)<8:
            messages.error(req,  "Password should be at least 8 characters!")
            return render(req, 'common/register.html')
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.warning(req, 'Password must contain at least one letter and one number')
            return render(req, 'common/register.html')
        try:
            user = CustomUser.objects.create_user(first_name=fname, last_name=lname, city=city, gender=gender, profile_img = profile_img, username=uname, email=email, user_type=user_type, password=confirm_password)
            messages.success(req,  'User Created Successfully')
            return redirect('loginPage')
        except IntegrityError:
            messages.error(req, 'Username already exists')
            return render(req, 'common/register.html')


    return render(req, 'common/register.html')     


# for loginPage with validations
def loginPage(req):
    if req.method=='POST':
        username = req.POST.get('uname')
        password = req.POST.get('pass')
        if not all([username, password]):
            messages.error(req, 'Please fill all the fields')
            return render(req, 'common/login.html')
        else: 
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                messages.success(req, 'Login Success!')
                return redirect('home')
            else: 
                messages.warning(req,  'Invalid Credentials')
                return render(req, 'common/login.html')

    return render(req, 'common/login.html')

# for home page
def home(req):
    data = JobModel.objects.all()
    context = {
        'jobs': data,
    }
    return render(req, 'common/index.html', context)
# for contact page
@login_required
def contact(req):
    return render(req, 'common/contact.html')


# for profile page for authentic users
@login_required
def profile(req):
    current_user = req.user
    data = CustomUser.objects.get(id=current_user.id)
    
    try:
        basic_info = get_object_or_404(BasicInfo, user=req.user)
        
    except Http404:
        messages.warning(req, "you don't have any basic information, please add information")
        return render(req, 'common/profile.html')

    context = {
        'data':data,
        'basic_info':basic_info
    }

    return render(req, 'common/profile.html', context)
# for logoutPage 
@login_required
def logoutPage(req):
    logout(req)
    messages.success(req, 'Logout Successful!')
    return redirect('login')
# for add_basic_info authentic users
@login_required
def add_basic_info(req):
    if req.user.user_type == "seeker" or req.user.user_type == 'recruiter':
        current_user = req.user
        if req.method == "POST":
            designation = req.POST.get('designation')
            contact_no = req.POST.get('contact_no')
            present_address = req.POST.get('present_address')
            permanent_address = req.POST.get('permanent_address')
            if current_user.user_type == "recruiter":
                com_web = req.POST.get('com_web')
                linkedin = req.POST.get('linkedin')
            career_summary = req.POST.get('career_summary')
            age = req.POST.get('age')
            dob = req.POST.get('dob')
            
            add_basic_info = BasicInfo(
                user=current_user,
                designation = designation,
                contact_no = contact_no,
                present_address = present_address,
                permanent_address = permanent_address,
                company_website = com_web,
                linkedin = linkedin,
                career_summary = career_summary,
                age = age,
                dob = dob,
            )
            current_user.save()
            
            add_basic_info.save()
            messages.success(req, "Basic Info Added Successfully")
            return redirect('profile')
            
    
    return render(req, 'common/add_basic_info.html',{'data':current_user})

# for edit_basic_info authentic users
@login_required
def edit_basic_info(req, id):
    current_user = req.user
    try: 
        data = get_object_or_404(BasicInfo, id=id)
    except Http404:
        messages.warning(req, "You have some problem to go to the edit option page.")
        return redirect('profile')    
    
    if req.user.user_type == "seeker" or req.user.user_type == 'recruiter':
        current_user = req.user
        if req.method == "POST":
            id = req.POST.get('basic_info_id')
            designation = req.POST.get('designation')
            contact_no = req.POST.get('contact_no')
            present_address = req.POST.get('present_address')
            permanent_address = req.POST.get('permanent_address')
            if current_user.user_type == "recruiter":
                com_web = req.POST.get('com_web')
                linkedin = req.POST.get('linkedin')
            career_summary = req.POST.get('career_summary')
            age = req.POST.get('age')
            dob = req.POST.get('dob')
            picture_new = req.FILES.get('picture_new')
            picture_old = req.POST.get('picture_old')
            
            basic_info_update = BasicInfo(
                id = id,
                user=current_user,
                designation = designation,
                contact_no = contact_no,
                present_address = present_address,
                permanent_address = permanent_address,
                company_website = com_web,
                linkedin = linkedin,
                career_summary = career_summary,
                age = age,
                dob = dob,

            )
            if picture_new:
                basic_info_update.picture = picture_new
            else:
                basic_info_update.picture = picture_old

            current_user.save()
            
            basic_info_update.save()
            messages.success(req, "Basic Info Updated Successfully")
            return redirect('profile')

    context = {
        'data':data
    }
    
    return render(req, 'common/edit_basic_info.html', context)

# for add_job page for recruiters functionality
@login_required
def add_job(req):
    current_user = req.user
    if current_user.user_type == "recruiter":
        if req.method == "POST":
            job_title = req.POST.get('job_title')
            emp_type = req.POST.get('employmentType')
            job_description = req.POST.get('job_description')
            job_location = req.POST.get('job_location')
            company_logo = req.FILES.get("company_logo")
            company_name = req.POST.get("company_name")
            salary = req.POST.get("salary")
            qualifications = req.POST.get("qualifications")
            deadline = req.POST.get("deadline")
            
            add_job = JobModel(
                user = current_user,
                job_title = job_title,
                job_type = emp_type,
                job_description = job_description,
                job_location = job_location,
                company_logo = company_logo,
                company_name = company_name,
                salary = salary,
                qualifications = qualifications,
                deadline = deadline
            )
            
            add_job.save()
            messages.success(req, "Job Posted Success")
            return redirect('job_feed')

    return render(req, "myAdmin/add_job.html")


# for job_delete for recruiters
@login_required  
def job_delete(req,id):
    current_user = req.user
    if current_user.user_type == "recruiter":
        data=JobModel.objects.filter(user=current_user, id=id)
        data.delete()
        messages.success(req, "Your Job Deleted Success")
        return redirect('created_job_by_recruiter')

# for edit_job functionality for recruiters in job_edit
@login_required
def job_edit(req, id):
    current_user = req.user
    if current_user.user_type == "recruiter":
        job = JobModel.objects.filter(user=current_user, id=id)
        if req.method == "POST":
            job_title = req.POST.get('job_title')
            id = id 
            emp_type = req.POST.get('employmentType')
            job_description = req.POST.get('job_description')
            job_location = req.POST.get('job_location')
            company_logo_old = req.POST.get("old_company_logo")
            company_logo_new = req.FILES.get("new_company_logo")
            company_name = req.POST.get("company_name")
            salary = req.POST.get("salary")
            qualifications = req.POST.get("qualifications")
            deadline = req.POST.get("deadline")
            
            job_update = JobModel(
                user = current_user,
                id = id,
                job_title = job_title,
                job_type = emp_type,
                job_description = job_description,
                job_location = job_location,
                company_name = company_name,
                salary = salary,
                qualifications = qualifications,
                deadline = deadline
            )
            if company_logo_new:
                job_update.company_logo = company_logo_new
            else:
                job_update.company_logo = company_logo_old
            
            job_update.save()
            messages.success(req, "Job Update Success")
            return redirect('created_job_by_recruiter')
        
        
        context={
            'data':job,
            'user':current_user
        }
        
    return render(req, "myAdmin/edit_job.html", context)
    
# for job-list page get all job data from database for job_feed
def job_feed(req):
    data = JobModel.objects.all()
    context = {
        'jobs':data
    }
    return render(req, "common/job-list.html", context)
    

# for createdJobByRecruiter page for recruiter get all job data from database
@login_required
def createdJobByRecruiter(req):
    if req.user.user_type == 'recruiter':
        current_user =  req.user
        job = JobModel.objects.filter(user=current_user)
        
        context = {
            'jobs':job
        }
    return render(req, "myAdmin/createdJobByRecruiter.html", context)       
        

# applyNow job page functionality for seeker in apply_now method
@login_required
def apply_now(req, id):
    current_user = req.user
    if current_user:
        # single job get
        current_job =  JobModel.objects.get(id=id)
        #which job that are matching and also filtered with applynow model if already apply.
        already_apply = ApplyNowModel.objects.filter(user=current_user, job=id)
        # counting the applicants
        applicants_counting =  ApplyNowModel.objects.filter(job=id).count()


        try:
            data = get_object_or_404(JobModel, id=id)
        except Http404:
            messages.error(req, "there is something wrong")
            return redirect('home')
            
        if current_user.user_type == 'seeker':
            if req.method == "POST":
                if already_apply.exists():
                    messages.error(req, "you have already applied for this job")    
                    
                else: 
                    applicant_name = req.POST.get('fullName')
                    applicant_email = req.POST.get('email')
                    applicant_cv = req.FILES.get('resume')
                    cover_letter = req.POST.get('coverLetter')
                    
                    applicant_create = ApplyNowModel(
                        user = current_user,
                        job = current_job,
                        applicant_name=applicant_name,
                        applicant_email=applicant_email,
                        applicant_cv=applicant_cv,
                        applicant_cover_letter=cover_letter,
                        
                    )
                    
                    applicant_create.save()
                    messages.success(req, 'Application Sent Successful')

                    return redirect('profile')
        

        context = {
            'data': data,
            'already_apply':already_apply,
            "applicants_counting":applicants_counting
        }
    else: 
        messages.warning(req, "you are not a user of this site Please Login or register")
        return redirect("loginPage")
    return render(req,  'common/applyNow.html', context)


# for applied_jobs page which are applied from seeker.
@login_required
def applied_jobs(req):
    current_user = req.user
    if current_user:
        try: 
            job = ApplyNowModel.objects.filter(user=current_user)

        except Http404:
            messages.error(req, "there is something wrong")
            return redirect('profile')
        context={
            "jobs":job
        }

    return render(req, "common/applied_jobs.html", context)







# search_job
def search_job(req):
    query = req.GET.get('search')
    if query: 
        job = JobModel.objects.filter(Q(job_title__icontains = query)|Q(job_description__icontains = query)|Q(job_location__icontains = query)|Q(company_name__icontains=query)|Q(salary__icontains = query))
        
    else:
        job = JobModel.objects.none()
        
    context = {
        'job':job,
        'query':query
    } 
    
    return render(req, 'common/search_job.html', context)    

# view_application from seeker that send for the job
@login_required
def view_application(req, id):
    job = JobModel.objects.get(id=id)
    applications = ApplyNowModel.objects.filter(job=job)
    current_user = req.user
    if current_user.user_type == 'seeker':
            if req.method == "POST":
                applicant_name = req.POST.get('fullName')
                apply_now_id = req.POST.get('apply_now_id')
                applicant_email = req.POST.get('email')
                applicant_cv_old = req.POST.get('applicant_cv_old')
                applicant_cv_new = req.FILES.get('resume')
                cover_letter = req.POST.get('coverLetter')
                
                applicant_update = ApplyNowModel(
                    user = current_user,
                    job = job,
                    id = apply_now_id,
                    applicant_name=applicant_name,
                    applicant_email=applicant_email,
                    applicant_cover_letter=cover_letter,
                    
                )

                if applicant_cv_new:
                    applicant_update.applicant_cv = applicant_cv_new
                else:
                    applicant_update.applicant_cv = applicant_cv_old
                
                applicant_update.save()
                messages.success(req, 'Application Updated Successful')

                return redirect('profile')
            else:
                messages.error(req, "something went wrong, Please try again later")

    return render(req, 'common/view_application.html', {'data': job, 'applications': applications})


# seeker can delete_applications for that job that he was applied
@login_required
def delete_applications(req, id):
    apply_now = ApplyNowModel.objects.get(id=id)
    apply_now.delete()
    messages.success(req, "Application deleted Success")
    return redirect('profile')


# for seeker my_settings
@login_required
def my_settings(req):
    current_user = req.user
    if current_user.user_type == 'seeker':
        education = EducationModel.objects.filter(user=current_user)
        skills = SkillModel.objects.filter(user=current_user)
        experience = ExperienceModel.objects.filter(user=current_user)
        language = LanguageModel.objects.filter(user=current_user)
        interest = InterestModel.objects.filter(user=current_user)

        context = {
            'education': education,
            'skills': skills,
            'experience': experience,
            'language': language,
            'interest': interest
        }


        return render(req, "common/my_settings.html", context)

# for add_education by seeker functionaity
@login_required
def add_education(req):
    if req.user.user_type == "seeker":
        degree = DegreeModel.objects.all()
        
        
        current_user = req.user
        try: 
            
            if req.method == "POST":
                institution_name = req.POST.get('institute_name')
                degree_id = req.POST.get('degree')
                degree_instance = DegreeModel.objects.get(id=degree_id)
                degree_name = degree_instance.name 
                field_of_study = req.POST.get('field_of_study')
                start_date = req.POST.get('start_date')
                end_date = req.POST.get('end_date')

                education_add = EducationModel(
                    user = current_user,
                    institution_name = institution_name,
                    degree = degree_name,
                    field_of_study = field_of_study,
                    start_date = start_date,
                    end_date = end_date
                )

                education_add.save()
                messages.success(req, "Education Added Success")
                return redirect('my_settings')
        except IntegrityError:
            messages.error(req, "Education is already exists")
            return render(req, "common/add_education.html")            

    context = {
        "degree":degree,
    }

    return render(req, "common/add_education.html", context)    


# for deleteEducation for seeker
@login_required
def deleteEducation(req, id):
    data = EducationModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Education Deleted Success")
    return redirect('my_settings')

# for edit_education for seeker in editEducation method
@login_required
def editEducation(req, id):
    if req.user.user_type == "seeker":
        degree = DegreeModel.objects.all()
        current_user = req.user
        try: 
            data = get_object_or_404(EducationModel, id=id)
            if req.method == "POST":
                institution_name = req.POST.get('institute_name')
                id = req.POST.get('education_id')
                degree_id = req.POST.get('degree')
                degree_instance = DegreeModel.objects.get(id=degree_id)
                degree_name = degree_instance.name
                field_of_study = req.POST.get('field_of_study')
                start_date = req.POST.get('start_date')
                end_date = req.POST.get('end_date')

                education_add = EducationModel(
                    user = current_user,
                    id = id,
                    institution_name = institution_name,
                    degree = degree_name,
                    field_of_study = field_of_study,
                    start_date = start_date,
                    end_date = end_date

                )

                education_add.save()
                messages.success(req, "Education Updated Success")
                return redirect('my_settings')
        except IntegrityError:
            messages.error(req, "Education is already exists")
            return render(req, "common/add_education.html")            

    context = {
        "degree":degree,
        'education':data,
    }
    return render(req, "common/edit_education.html", context)

# for add_experience  for seeker in addExperience method
@login_required
def addExperience(request):
    if request.user.user_type == "seeker":
        current_user = request.user
        try: 
            if request.method == "POST":
                job_title = request.POST.get('job_title')
                company_name = request.POST.get('company_name')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                description = request.POST.get('description')

                experience_add = ExperienceModel(
                    user = current_user,
                    job_title = job_title,
                    company_name = company_name,
                    start_date = start_date,
                    end_date = end_date,
                    description = description

                )

                experience_add.save()
                messages.success(request, "Experience Added Success")
                return redirect('my_settings')
        except IntegrityError:
            messages.error(request, "Experience is already exists")
            return render(request, "common/add_experience.html") 

    return render(request, "common/add_experience.html")

# deleteExperience for seeker
@login_required
def deleteExperience(req, id):
    data = ExperienceModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Experience Deleted Success")
    return redirect('my_settings')

# edit_experience for seeker in editExperience method
@login_required
def editExperience(request, id):
    if request.user.user_type == "seeker":
        current_user = request.user
        try: 
            data = get_object_or_404(ExperienceModel, id=id)
            if request.method == "POST":
                job_title = request.POST.get('job_title')
                id = request.POST.get('experience_id')
                company_name = request.POST.get('company_name')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                description = request.POST.get('description')

                experience_update = ExperienceModel(
                    user = current_user,
                    id = id,
                    job_title = job_title,
                    company_name = company_name,
                    start_date = start_date,
                    end_date = end_date,
                    description = description

                )

                experience_update.save()
                messages.success(request, "Experience Updated Success")
                return redirect('my_settings')
        except IntegrityError:
            messages.error(request, "Experience is already exists")
            return render(request, "common/edit_experience.html")

    context = {
        'experience':data
    }     

    return render(request, "common/edit_experience.html", context)




# add_skill page functionality in add_skills method
@login_required
def add_skills(req):
    current_user = req.user
    if req.user.user_type == "recruiter" or req.user.user_type == "seeker":
        all_skills = IntermediateSkillModel.objects.all()
        
        context = {
            'all_skills': all_skills
        }
        if req.method == 'POST':
            skill_id = req.POST.get('skill_id')
            skill_level = req.POST.get('skill_level')
            skill_obj = get_object_or_404(IntermediateSkillModel, id=skill_id)
            if SkillModel.objects.filter(user=current_user, skill_name=skill_obj).exists():
                messages.warning(req, 'This skill is already added.')
                return render(req, 'common/add_skill.html')
            else: 
                skill_add = SkillModel(
                    user = current_user,
                    skill_name = skill_obj.skill_name,
                    skill_level = skill_level
                )

                skill_add.save()
                return redirect('my_settings')
    return render(req, 'common/add_skill.html', context)

# deleteSkill functionality
@login_required
def deleteSkill(req, id):
    data = SkillModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Skill Deleted Success")
    return redirect('my_settings')

# edit_skill page functionality in edit_skills method 
@login_required
def edit_skills(req, id):
    current_user = req.user
    if req.user.user_type == "recruiter" or req.user.user_type == "seeker":
        all_skills = IntermediateSkillModel.objects.all()
        skills = get_object_or_404(SkillModel, id=id)
        skill_id = skills.id
        print(skill_id)
        
        context = {
            'all_skills': all_skills,
            'skill':skills,
        }
        if req.method == 'POST':
            skill_id = req.POST.get('skill_id')
            id = req.POST.get('id')
            skill_level = req.POST.get('skill_level')
            skill_obj = get_object_or_404(IntermediateSkillModel, id=skill_id)
            if SkillModel.objects.filter(user=current_user, skill_name=skill_obj).exists():
                messages.warning(req, 'This skill is already added.')
                return redirect('my_settings')
            else: 
                skill_update = SkillModel(
                    user = current_user,
                    id = id,
                    skill_name = skill_obj.skill_name,
                    skill_level = skill_level
                )

                skill_update.save()
                messages.success(req, 'Skill updated.')
                return redirect('my_settings')
    return render(req, 'common/edit_skill.html', context)

# add_language page functionality in addLanguage method
@login_required
def addLanguage(request):

    if request.user.user_type == "seeker":
        current_user = request.user
    try: 

        if request.method == "POST":
            language_name = request.POST.get('language_name')
            language_level = request.POST.get('lang_level')

            language_add = LanguageModel(
                user = current_user,
                language_name = language_name,
                language_level = language_level,
            )

            language_add.save()
            messages.success(request, "Language Added Success")
            return redirect('my_settings')
    except IntegrityError:
        messages.error(request, "Language is already exists")
        return redirect('my_settings')



    return render(request, "common/add_language.html")

# deleteLanguage functionality
@login_required
def deleteLanguage(req, id):
    data = LanguageModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Language Deleted Success")
    return redirect('my_settings')

# edit_language page functionality in editLanguage method

@login_required
def editLanguage(req, id):
    current_user = req.user
    try: 
        data = get_object_or_404(LanguageModel, id=id)
    except Http404:
        messages.warning(req, "You have some problem to go to the edit option page.")
        return redirect('my_settings')   
    if req.method == "POST":
        language_name = req.POST.get('language_name')
        language_level = req.POST.get('lang_level')
        id = req.POST.get('language_id')

        update_language = LanguageModel(
            user = current_user,
            id = id,
            language_name = language_name,
            language_level = language_level,

        )
        update_language.save()
        messages.success(req, "Language Updated Success")
        return redirect('my_settings')
    
    context = {
        'language':data
    }
    return render(req, "common/edit_language.html", context)

# add_interest  functionality  in addInterest method


@login_required
def addInterest(request):
    if request.user.user_type == "seeker":
        current_user = request.user
    try: 
        if request.method == "POST":
            interest_name = request.POST.get('interest_name')
            description = request.POST.get('description')

            interest_add = InterestModel(
                user = current_user,
                interest_name = interest_name,
                description = description,
            )

            interest_add.save()
            messages.success(request, "Interest Added Success")
            return redirect('my_settings')
    except IntegrityError:
        messages.error(request, "Interest is already exists")
        return render(request, "common/add_interest.html") 



    return render(request, "common/add_interest.html")


# deleteInterest functionality

@login_required
def deleteInterest(req, id):
    data =  InterestModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Interest Deleted Success")
    return redirect('my_settings')

# edit_interest functionaliy in editInterest method

@login_required
def editInterest(req, id):
    current_user = req.user
    try: 
        data = get_object_or_404(InterestModel, id=id)
    except Http404:
        messages.warning(req, "You have some problem to go to the edit option page.")
        return redirect('my_settings')   
    if req.method == "POST":
        interest_name = req.POST.get('interest_name')
        description = req.POST.get('description')
        id = req.POST.get('interest_id')

        update_interest = InterestModel(
            user = current_user,
            id = id,
            interest_name = interest_name,
            description = description,

        )

        update_interest.save()
        messages.success(req, "Interest Updated Success")
        return redirect('my_settings')
    
    context = {
        'interest':data
    }

    return render(req, "common/edit_interest.html", context)

#  change_password functionality in changePassword method
@login_required
def changePassword(req):
    current_user = req.user
    if req.method == "POST":
        old_password = req.POST.get('old_password')
        new_password = req.POST.get('new_password')
        confirm_password = req.POST.get('confirm_password')

        if check_password(old_password, current_user.password):
            if new_password != confirm_password:
                messages.error(req, "New Password And Confirm Password Doesn't Match.")
                return render(req,  "common/change_password.html")
            elif old_password == new_password or old_password == confirm_password:
                messages.error(req, "Old Password And New Password Can't Be Same.")
                return render(req,  "common/change_password.html")
            else:
                current_user.set_password(confirm_password)
                current_user.save()
                messages.success(req, "Password Reset Success")
                return render(req,  "common/change_password.html")

    return render(req,  "common/change_password.html")















