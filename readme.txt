-------at end ------pip freeze > requirements.txt

1. Start with python virtual box:
-----------------------------------------------------------------------------------------------
python3 -m venv venv

source venv/bin/activate

-----------------------------------------------------------------------------------------------

2.  pip install django
    django-admin startproject student_task_manager .

-----------------------------------------------------------------------------------------------

3.  python manage.py startapp tasks
    python manage.py startapp accounts

-----------------------------------------------------------------------------------------------

4.  python manage.py makemigrations
    python manage.py migrate

-----------------------------------------------------------------------------------------------

5. to test: python manage.py shell
                                    from accounts.models import User
                                    from tasks.models import Semester, Course
                                    from datetime import date

                                    # Get or create a user
                                    user = User.objects.first()
                                    if not user:
                                        user = User.objects.create(
                                            username="testuser",
                                            email="test@example.com",
                                            password="hashedpassword123",
                                            first_name="Test",
                                            last_name="User"
                                        )

                                    # Create semester
                                    sem = Semester.objects.create(
                                        user=user,
                                        name="Fall 2026",
                                        start_date=date(2026, 9, 1),
                                        end_date=date(2026, 12, 15)
                                    )

                                    print("✅ Semester created:", sem.name)

                                    # Create course
                                    course = Course.objects.create(
                                        semester=sem,
                                        name="Calculus",
                                        code="MATH101",
                                        instructor="Dr. Smith",
                                        credits=3
                                    )

                                    print("✅ Course created:", course.name)

                                    # Check relationship
                                    print("✅ Courses in semester:", sem.course_set.all())

                                    # Test HabitCheckin with unique_together
                                    from tasks.models import Habit, HabitCheckin
                                    from django.utils import timezone

                                    habit = Habit.objects.create(user=user, name="Morning Exercise")
                                    print("✅ Habit created:", habit.name)

                                    checkin = HabitCheckin.objects.create(
                                        habit=habit,
                                        date=date.today(),
                                        checked=True
                                    )
                                    print("✅ HabitCheckin created for today")

                                    # Try creating duplicate (should fail)
                                    try:
                                        checkin2 = HabitCheckin.objects.create(
                                            habit=habit,
                                            date=date.today(),
                                            checked=False
                                        )
                                    except Exception as e:
                                        print("❌ Duplicate prevented (good!):", type(e).__name__)

                                    print("\n✅ All tests passed!")
6. 
