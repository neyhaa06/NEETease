
from pathlib import Path
import time

import joblib
import pandas as pd

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import TestResult, StudentProfile, SubjectResult, WellbeingEntry


def home(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "index.html")


def signup_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if User.objects.filter(username=email).exists():
            messages.error(
                request,
                "An account with this email already exists."
            )
            return render(request, "signup.html")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        StudentProfile.objects.create(
            user=user,
            mobile=mobile
        )

        messages.success(
            request,
            "Account created successfully! Please log in."
        )

        return redirect("home")

    return render(request, "signup.html")


def dashboard(request):
    return render(request, "dashboard.html")


def study_materials(request):
    return render(request, "study_materials.html")


def biology(request):
    return render(request, "biology.html")


def chemistry(request):
    return render(request, "chemistry.html")


def physics(request):
    return render(request, "physics.html")


@login_required
def analytics(request):
    # Get only this student's saved test results.
    all_results = list(
        TestResult.objects.filter(
            user=request.user
        ).order_by("-completed_at")
    )

    tests_attempted = len(all_results)

    questions_attempted = sum(
        result.total_questions for result in all_results
    )

    if tests_attempted > 0:
        average_accuracy = round(
            sum(result.accuracy for result in all_results)
            / tests_attempted
        )
    else:
        average_accuracy = 0

    best_result = (
        max(all_results, key=lambda result: result.accuracy)
        if all_results else None
    )

    recent_results = list(reversed(all_results[:7]))

    chart_data = [
        {
            "label": result.test_name,
            "accuracy": result.accuracy,
        }
        for result in recent_results
    ]

    analytics_insights = []

    if not all_results:
        analytics_insights.append(
            "Complete a mock test to start receiving "
            "personalized performance insights."
        )
    else:
        if average_accuracy >= 80:
            analytics_insights.append(
                "Your average accuracy is strong. "
                "Keep revising regularly to maintain your progress."
            )
        elif average_accuracy >= 60:
            analytics_insights.append(
                "You have a developing foundation. "
                "Review incorrect answers and practise weak topics."
            )
        else:
            analytics_insights.append(
                "Focus on understanding concepts and reviewing "
                "mistakes before attempting more questions."
            )

        if len(recent_results) >= 2:
            previous_accuracy = recent_results[-2].accuracy
            latest_accuracy = recent_results[-1].accuracy

            if latest_accuracy > previous_accuracy:
                analytics_insights.append(
                    "Your latest test accuracy improved compared "
                    "with the previous test."
                )
            elif latest_accuracy < previous_accuracy:
                analytics_insights.append(
                    "Your latest test accuracy decreased compared "
                    "with the previous test. Review the questions "
                    "you found difficult."
                )
            else:
                analytics_insights.append(
                    "Your latest test accuracy matches the previous "
                    "test. Keep practising to build consistency."
                )

    # Generate personalized study recommendations.
    study_recommendations = []

    if not all_results:
        study_recommendations.append(
            "Start with a mock test to establish your current "
            "performance level."
        )
    else:
        if average_accuracy < 60:
            study_recommendations.append(
                "Revise the fundamental concepts covered in your "
                "tests before moving to more difficult questions."
            )
            study_recommendations.append(
                "Practise small sets of questions and review each "
                "incorrect answer carefully."
            )
        elif average_accuracy < 80:
            study_recommendations.append(
                "Review the questions you answered incorrectly "
                "and revise the concepts behind those mistakes."
            )
            study_recommendations.append(
                "Practise timed question sets to improve accuracy "
                "while managing your time."
            )
        else:
            study_recommendations.append(
                "Maintain your progress with regular revision "
                "and timed mock tests."
            )
            study_recommendations.append(
                "Challenge yourself with unfamiliar questions "
                "to strengthen your understanding."
            )

        if len(all_results) >= 2:
            latest_accuracy = all_results[0].accuracy
            previous_accuracy = all_results[1].accuracy

            if latest_accuracy < previous_accuracy:
                study_recommendations.append(
                    "Your latest test score is lower than the "
                    "previous one. Revisit the topics covered "
                    "in that test and identify possible mistakes."
                )
            elif latest_accuracy > previous_accuracy:
                study_recommendations.append(
                    "Your latest test score improved. Continue "
                    "using the study methods that are helping you."
                )
            else:
                study_recommendations.append(
                    "Your last two test accuracies are equal. "
                    "Review recurring mistakes to find areas "
                    "where you can improve."
                )

        if tests_attempted < 3:
            study_recommendations.append(
                "Complete a few more mock tests to build a "
                "clearer picture of your performance over time."
            )

    # Calculate subject-wise performance from saved test data.
    subject_analytics = []

    for subject_name in ["Biology", "Chemistry", "Physics"]:
        subject_results = SubjectResult.objects.filter(
            test_result__user=request.user,
            subject=subject_name
        )

        total_score = sum(
            result.score for result in subject_results
        )

        total_questions = sum(
            result.total_questions for result in subject_results
        )

        accuracy = (
            round(total_score / total_questions * 100)
            if total_questions > 0 else None
        )

        subject_analytics.append({
            "subject": subject_name,
            "accuracy": accuracy,
            "questions_attempted": total_questions,
            "tests_attempted": subject_results.values(
                "test_result_id"
            ).distinct().count(),
        })

    context = {
        "results": all_results,
        "tests_attempted": tests_attempted,
        "best_result": best_result,
        "questions_attempted": questions_attempted,
        "average_accuracy": average_accuracy,
        "chart_data": chart_data,
        "analytics_insights": analytics_insights,
        "study_recommendations": study_recommendations,
        "subject_analytics": subject_analytics,
    }

    return render(request, "analytics.html", context)


@login_required

@login_required
def wellbeing(request):
    success = None
    error = None

    # ML prediction results
    prediction = None
    prediction_probabilities = None
    prediction_error = None

    if request.method == "POST":
        form_type = request.POST.get("form_type", "checkin")

        # ---------------------------------------------
        # ML LIFESTYLE PREDICTION
        # ---------------------------------------------
        if form_type == "ml_prediction":
            try:
                study_hours_ml = float(
                    request.POST.get("study_hours_ml", "")
                )
                extracurricular_hours = float(
                    request.POST.get("extracurricular_hours", "")
                )
                sleep_hours_ml = float(
                    request.POST.get("sleep_hours_ml", "")
                )
                social_hours = float(
                    request.POST.get("social_hours", "")
                )
                physical_activity_hours = float(
                    request.POST.get("physical_activity_hours", "")
                )

                values = [
                    study_hours_ml,
                    extracurricular_hours,
                    sleep_hours_ml,
                    social_hours,
                    physical_activity_hours,
                ]

                if any(
                    not 0 <= value <= 24
                    for value in values
                ):
                    raise ValueError

                # A day contains only 24 hours in total.
                if sum(values) > 24:
                    prediction_error = (
                        "The five daily activities cannot total "
                        "more than 24 hours. Please check your entries."
                    )
                else:
                    model_path = (
                        Path(settings.BASE_DIR)
                        / "ml"
                        / "artifacts"
                        / "stress_classifier.joblib"
                    )

                    if not model_path.exists():
                        raise FileNotFoundError

                    model_bundle = joblib.load(model_path)
                    model = model_bundle["model"]

                    feature_columns = model_bundle.get(
                        "feature_columns",
                        [
                            "Study_Hours_Per_Day",
                            "Extracurricular_Hours_Per_Day",
                            "Sleep_Hours_Per_Day",
                            "Social_Hours_Per_Day",
                            "Physical_Activity_Hours_Per_Day",
                        ],
                    )

                    input_values = {
                        "Study_Hours_Per_Day": study_hours_ml,
                        "Extracurricular_Hours_Per_Day":
                            extracurricular_hours,
                        "Sleep_Hours_Per_Day": sleep_hours_ml,
                        "Social_Hours_Per_Day": social_hours,
                        "Physical_Activity_Hours_Per_Day":
                            physical_activity_hours,
                    }

                    input_data = pd.DataFrame(
                        [[input_values[column]
                          for column in feature_columns]],
                        columns=feature_columns,
                    )

                    predicted_category = model.predict(input_data)[0]
                    probabilities = model.predict_proba(input_data)[0]

                    prediction = str(predicted_category)

                    prediction_probabilities = {
                        str(category): round(
                            float(probability) * 100, 1
                        )
                        for category, probability in zip(
                            model.classes_,
                            probabilities,
                        )
                    }

            except (TypeError, ValueError):
                prediction_error = (
                    "Please enter valid numbers between 0 and 24 "
                    "for all five lifestyle fields."
                )

            except FileNotFoundError:
                prediction_error = (
                    "The trained ML model file could not be found. "
                    "Check ml/artifacts/stress_classifier.joblib."
                )

            except Exception:
                prediction_error = (
                    "The prediction could not be completed. "
                    "Please check the model setup and try again."
                )

        # ---------------------------------------------
        # EXISTING DAILY CHECK-IN
        # ---------------------------------------------
        else:
            mood = request.POST.get("mood")
            stress_level = request.POST.get("stress_level")
            sleep_hours = request.POST.get("sleep_hours")
            study_hours = request.POST.get("study_hours")

            valid_moods = {
                "great", "good", "okay", "stressed", "tired"
            }

            try:
                stress_level = int(stress_level)
                sleep_hours = float(sleep_hours)
                study_hours = float(study_hours)

                if (
                    mood not in valid_moods
                    or not 1 <= stress_level <= 10
                    or not 0 <= sleep_hours <= 24
                    or not 0 <= study_hours <= 24
                ):
                    raise ValueError

            except (TypeError, ValueError):
                error = "Please enter valid values for all fields."

            else:
                WellbeingEntry.objects.create(
                    user=request.user,
                    mood=mood,
                    stress_level=stress_level,
                    sleep_hours=sleep_hours,
                    study_hours=study_hours,
                )

                success = "Your well-being check-in has been saved!"

    # ---------------------------------------------
    # RETRIEVE EXISTING CHECK-INS
    # ---------------------------------------------
    entries = list(
        WellbeingEntry.objects.filter(user=request.user)
        .order_by("-created_at")
    )

    recent_entries = entries[:10]

    # Charts use up to seven entries, oldest to newest.
    trend_entries = list(reversed(entries[:7]))

    # Match the displayed average summary to the latest five entries.
    summary_entries = entries[:5]

    if summary_entries:
        count = len(summary_entries)

        average_stress = round(
            sum(e.stress_level for e in summary_entries) / count, 1
        )
        average_sleep = round(
            sum(float(e.sleep_hours) for e in summary_entries) / count, 1
        )
        average_study = round(
            sum(float(e.study_hours) for e in summary_entries) / count, 1
        )
    else:
        average_stress = None
        average_sleep = None
        average_study = None

    # ---------------------------------------------
    # PERSONALIZED INSIGHTS
    # ---------------------------------------------
    wellbeing_insights = []

    if summary_entries:
        # Stress pattern
        if average_stress >= 7:
            wellbeing_insights.append(
                "Your recent stress scores are relatively high. "
                "Consider breaking study sessions into manageable "
                "blocks and making time for rest."
            )
        elif average_stress <= 3:
            wellbeing_insights.append(
                "Your recent stress scores are relatively low. "
                "Continue checking in with yourself as your routine changes."
            )
        else:
            wellbeing_insights.append(
                "Your recent stress scores are in a moderate range. "
                "Keep monitoring how you feel during preparation."
            )

        # Sleep pattern
        if average_sleep < 6:
            wellbeing_insights.append(
                f"Your recent sleep average is {average_sleep} hours. "
                "Consider making more time for rest and maintaining "
                "a consistent sleep routine."
            )
        elif average_sleep < 7:
            wellbeing_insights.append(
                f"You are averaging {average_sleep} hours of sleep. "
                "Review whether you feel rested and whether your routine "
                "allows enough sleep."
            )
        else:
            wellbeing_insights.append(
                f"Your recent sleep average is {average_sleep} hours. "
                "Keep protecting your sleep routine as you prepare."
            )

        # Study pattern
        if average_study >= 8:
            wellbeing_insights.append(
                f"Your recorded study average is {average_study} hours. "
                "Plan short breaks and avoid sacrificing sleep for "
                "extra study time."
            )
        elif average_study < 2:
            wellbeing_insights.append(
                f"Your recorded study average is {average_study} hours. "
                "If it suits your schedule, try setting a small, "
                "realistic study goal."
            )
        else:
            wellbeing_insights.append(
                f"Your recorded study average is {average_study} hours. "
                "Aim for a sustainable balance between focused study, "
                "rest, and other activities."
            )

        # Mood pattern among the latest five check-ins
        tired_count = sum(
            entry.mood == "tired" for entry in summary_entries
        )
        stressed_mood_count = sum(
            entry.mood == "stressed" for entry in summary_entries
        )

        if tired_count >= 2:
            wellbeing_insights.append(
                "You selected 'Tired' in multiple recent check-ins. "
                "Consider reviewing your rest and break schedule."
            )

        if stressed_mood_count >= 2:
            wellbeing_insights.append(
                "You selected 'Stressed' in multiple recent check-ins. "
                "Try a short breathing break or talk with someone you trust "
                "if you feel you need support."
            )

        # Compare recent three check-ins with the preceding three.
        # entries are ordered newest first.
        if len(entries) >= 4:
            latest_three = entries[:3]
            previous_three = entries[3:6]

            latest_stress = sum(
                e.stress_level for e in latest_three
            ) / len(latest_three)

            previous_stress = sum(
                e.stress_level for e in previous_three
            ) / len(previous_three)

            latest_sleep = sum(
                float(e.sleep_hours) for e in latest_three
            ) / len(latest_three)

            previous_sleep = sum(
                float(e.sleep_hours) for e in previous_three
            ) / len(previous_three)

            if latest_stress >= previous_stress + 1:
                wellbeing_insights.append(
                    "Your latest three stress scores average higher "
                    "than the preceding check-ins. Consider whether "
                    "your workload or rest routine has changed."
                )
            elif latest_stress <= previous_stress - 1:
                wellbeing_insights.append(
                    "Your latest three stress scores are lower on average "
                    "than the preceding check-ins. Notice which routines "
                    "may be helping you feel better."
                )

            if latest_sleep <= previous_sleep - 1:
                wellbeing_insights.append(
                    "Your latest three check-ins show less sleep on average "
                    "than the preceding check-ins. Consider protecting "
                    "your sleep time."
                )
            elif latest_sleep >= previous_sleep + 1:
                wellbeing_insights.append(
                    "Your latest three check-ins show more sleep on average. "
                    "Continue observing whether this helps you feel rested."
                )

    else:
        wellbeing_insights.append(
            "Save a check-in to receive insights based on your own "
            "stress, sleep, and study patterns."
        )

    # Keep the ML estimate separate from self-reported check-in scores.
    if prediction:
        category = prediction.strip().lower()

        if category == "high":
            wellbeing_insights.append(
                "Your lifestyle-based model estimated the High category. "
                "This is an experimental dataset-based result, not a "
                "diagnosis. Review your routine and how you feel personally."
            )
        elif category == "moderate":
            wellbeing_insights.append(
                "Your lifestyle-based model estimated the Moderate category. "
                "Use this as an experimental estimate alongside your own "
                "check-ins, not as a diagnosis."
            )
        elif category == "low":
            wellbeing_insights.append(
                "Your lifestyle-based model estimated the Low category. "
                "This does not guarantee that you feel well; your own "
                "experience and check-ins still matter."
            )

    context = {
        "success": success,
        "error": error,
        "recent_entries": recent_entries,
        "trend_entries": trend_entries,
        "average_stress": average_stress,
        "average_sleep": average_sleep,
        "average_study": average_study,
        "wellbeing_insights": wellbeing_insights,
        "prediction": prediction,
        "prediction_probabilities": prediction_probabilities,
        "prediction_error": prediction_error,
    }

    return render(request, "wellbeing.html", context)


@login_required
def profile(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    return render(request, "profile.html", {
        "profile": profile
    })


@login_required
def edit_profile(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")

        request.user.first_name = full_name
        request.user.email = email
        request.user.username = email
        request.user.save()

        profile.mobile = mobile
        profile.save()

        messages.success(request, "Profile updated successfully!")

        return redirect("profile")

    return render(request, "edit_profile.html", {
        "profile": profile
    })


@login_required
def chatbot(request):
    return render(request, "chatbot.html")


def mock_tests(request):
    return render(request, "mock_tests.html")


def start_test(request):
    questions = [
        {
            "question": "Which organelle is known as the powerhouse of the cell?",
            "options": [
                "Nucleus", "Mitochondria", "Ribosome", "Golgi apparatus"
            ],
            "answer": "B",
            "subject": "Biology",
        },
        {
            "question": "What is the basic unit of life?",
            "options": [
                "Tissue", "Organ", "Cell", "Organ system"
            ],
            "answer": "C",
            "subject": "Biology",
        },
        {
            "question": "Which gas is released during photosynthesis?",
            "options": [
                "Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"
            ],
            "answer": "A",
            "subject": "Biology",
        },
        {
            "question": (
                "Which part of the human heart pumps oxygenated blood "
                "to the body?"
            ),
            "options": [
                "Right atrium",
                "Right ventricle",
                "Left atrium",
                "Left ventricle",
            ],
            "answer": "D",
            "subject": "Biology",
        },
        {
            "question": "Which molecule carries genetic information?",
            "options": [
                "DNA", "Glucose", "ATP", "Protein"
            ],
            "answer": "A",
            "subject": "Biology",
        },
    ]

    question_number = int(request.GET.get("q", 1))

    # Start a fresh test.
    if (
        question_number == 1
        and request.method == "GET"
        and "test_end_time" not in request.session
    ):
        request.session["answers"] = {}
        request.session["reviewed"] = []
        request.session["test_end_time"] = time.time() + (15 * 60)

    # Handle submitted answer.
    if request.method == "POST":
        selected_answer = request.POST.get("answer")

        answers = request.session.get("answers", {})
        reviewed = request.session.get("reviewed", [])

        if selected_answer:
            answers[str(question_number)] = selected_answer

        request.session["answers"] = answers

        if request.POST.get("review") == "yes":
            if question_number not in reviewed:
                reviewed.append(question_number)

        request.session["reviewed"] = reviewed

        # Finish the test on the last question.
        if question_number == len(questions):
            score = 0
            review = []

            for number, answer in answers.items():
                question_index = int(number) - 1
                question_data = questions[question_index]
                correct_answer = question_data["answer"]

                if answer == correct_answer:
                    score += 1
                    result = "Correct"
                else:
                    result = "Wrong"

                review.append({
                    "number": number,
                    "question": question_data["question"],
                    "selected": answer,
                    "correct": correct_answer,
                    "result": result,
                })

            accuracy = round((score / len(questions)) * 100)

            test_result = TestResult.objects.create(
                user=request.user,
                test_name="Full Syllabus Test",
                score=score,
                total_questions=len(questions),
                accuracy=accuracy,
            )

            # Calculate and save scores for each subject.
            subject_totals = {}

            for number, answer in answers.items():
                question_index = int(number) - 1
                question_data = questions[question_index]
                subject = question_data.get("subject", "Biology")

                if subject not in subject_totals:
                    subject_totals[subject] = {
                        "score": 0,
                        "total": 0,
                    }

                subject_totals[subject]["total"] += 1

                if answer == question_data["answer"]:
                    subject_totals[subject]["score"] += 1

            for subject, totals in subject_totals.items():
                subject_accuracy = round(
                    totals["score"] / totals["total"] * 100
                )

                SubjectResult.objects.create(
                    test_result=test_result,
                    subject=subject,
                    score=totals["score"],
                    total_questions=totals["total"],
                    accuracy=subject_accuracy,
                )

            # Clear the finished test session.
            request.session.pop("answers", None)
            request.session.pop("reviewed", None)
            request.session.pop("test_end_time", None)

            return render(request, "results.html", {
                "score": score,
                "total_questions": len(questions),
                "accuracy": accuracy,
                "review": review,
            })

        # Move to the next question.
        question_number += 1

    # Make sure the question number is valid.
    if question_number < 1:
        question_number = 1

    if question_number > len(questions):
        question_number = len(questions)

    question = questions[question_number - 1]

    answers = request.session.get("answers", {})
    selected_answer = answers.get(str(question_number))
    reviewed = request.session.get("reviewed", [])

    is_reviewed = question_number in reviewed

    return render(request, "test.html", {
        "question": question,
        "question_number": question_number,
        "total_questions": len(questions),
        "test_end_time": request.session.get("test_end_time", 0),
        "selected_answer": selected_answer,
        "is_reviewed": is_reviewed,
    })
