from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from .models import Job,JobApplication,APPLICATION_STATUS_CHOICES
from django.contrib import messages


# Create your views here.

@login_required
def job_create(request):
    if not request.user.role == 'recruiter':
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request,'Job Posted Successfully')
            return redirect('recruiter_dashboard')
    
    else:
        form = JobPostForm()
    
    return render(request,'jobs/jobs_create.html',{'form_data':form})

@login_required
def recruiter_job(request):
    if not request.user.role == 'recruiter':
        return redirect('student_dashboard')
    
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request,'jobs/recruiter_jobs.html',{'jobs':jobs})




def view_all_students_jobs(request):
    all_jobs = Job.objects.all().order_by('-created_at')
    # print(all_jobs)
    return render(request,'jobs/all_student_jobs.html',{'jobs':all_jobs})


def job_detail(request,id):
    job = get_object_or_404(Job,id=id)
    return render(request,'jobs/job_detail.html',{'job_data':job})


def apply_job(request,id):
    if not request.user.is_authenticated or not request.user.role == 'student':
        messages.error(request,"Only students can apply.")
        return redirect('login')
    
    job = get_object_or_404(Job,id=id)
    already_applied = JobApplication.objects.filter(job=job,student=request.user).exists()
    if already_applied:
        messages.warning(request,"You have already applied for this Job")
    else:
        JobApplication.objects.create(job=job,student=request.user)
        messages.success(request,"Successfully applied to the Job")
    
    return redirect('view_jobs')


@login_required
def edit_job(request,job_id):
    job = get_object_or_404(Job,id=job_id,posted_by=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST,instance=job)
        if form.is_valid():
            form.save()
            messages.success(request,"Job Updated Successfully")
            return redirect('recruiter_dashboard')
    else:
        form = JobPostForm(instance=job)
    return render(request,'jobs/edit_job.html',{'form_data':form})

@login_required
def delete_job(request,job_id):
    job = get_object_or_404(Job,id=job_id,posted_by=request.user)

    if request.method == 'POST':
        job.delete()
        messages.info(request,"Job Deleted Successfully")
        return redirect('recruiter_dashboard')

    return render(request,'jobs/recruiter_jobs.html',{'jobs':job})

@login_required
def view_applicants(request,job_id):
    job = get_object_or_404(Job,id=job_id,posted_by=request.user)
    applications = JobApplication.objects.filter(job=job).select_related('student')
    return render(request,'jobs/view_applicants.html',{'job':job,'applications':applications,'status_choices':APPLICATION_STATUS_CHOICES})


@login_required
def update_application_status(request,application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication,id=application_id)
        new_status = request.POST.get('status')
        if new_status in dict(APPLICATION_STATUS_CHOICES):
            print(f'104 {new_status}')
            application.status = new_status
            application.status_notified = False
            application.save()
            messages.success(request,f"Application status updated to {new_status.title()} successfully")
        else:
            messages.error(request,"Invalid Status Provided")
    return redirect('view_applicants',job_id=application.job.id)
        