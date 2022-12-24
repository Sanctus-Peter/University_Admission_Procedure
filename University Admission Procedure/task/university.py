# write your code here
from collections import defaultdict

max_admitted = int(input())
PHYSICS_COL = 2
CHEMISTRY_COL = 3
MATHEMATICS_COL = 4
COMPUTER_COL = 5
ADMISSION_SCORE = 6
SCORE = 10
COURSE1 = 7
COURSE2 = 8
COURSE3 = 9

with open("applicants.txt", "r") as file:
    applicants = [line.strip() for line in file.readlines()]

accepted = defaultdict(list)


def get_course_col(department):
    if department == "Physics":
        score_col = PHYSICS_COL
    elif department == "Chemistry" or department == "Biotech":
        score_col = CHEMISTRY_COL
    elif department == "Mathematics":
        score_col = MATHEMATICS_COL
    else:
        score_col = COMPUTER_COL
    return score_col


def get_aux_course(department):
    if department == "Physics":
        col = MATHEMATICS_COL
    elif department == "Biotech":
        col = PHYSICS_COL
    else:
        col = MATHEMATICS_COL
    return col


def get_ranking_list(bio_data: list) -> defaultdict:
    ranking = defaultdict(list)
    for students in bio_data:
        ranking[students.split()[COURSE1]].append(students)
        ranking[students.split()[COURSE2]].append(students)
        ranking[students.split()[COURSE3]].append(students)
    return ranking


def sort_applicants(applicants_list: list, score_col: int, aux_score: int) -> list:
    applicants_list.sort(key=lambda x: x.split()[0] + x.split()[1])
    applicants_list.sort(
        key=lambda x: x.split()[SCORE], reverse=True
    )
    return applicants_list


def get_scores(students: list, score_col, aux_score) -> list:
    for index, student in enumerate(students):
        if aux_score:
            admission_score = max(
                (float(student.split()[score_col]) + float(student.split()[aux_score])) / 2,
                float(student.split()[ADMISSION_SCORE])
            )
        else:
            admission_score = max(
                float(student.split()[score_col]), float(student.split()[ADMISSION_SCORE])
            )
        student = student + " " + str(admission_score)
        students[index] = student
    return students


def get_admitted(ranking: defaultdict, batch) -> defaultdict:
    for department in sorted(ranking.keys()):
        aux_score = None
        n_applicants = ranking[department]
        score_col = get_course_col(department)
        if department in ("Physics", "Biotech", "Engineering"):
            aux_score = get_aux_course(department)
        n_applicants = get_scores(n_applicants, score_col, aux_score)
        n_applicants = sort_applicants(n_applicants, score_col, aux_score)
        n_applicants.sort(key=lambda x: x.split()[batch])
        n = 0
        while len(accepted[department]) < max_admitted and n_applicants:
            if n >= len(n_applicants):
                break
            if n_applicants[n].split()[batch] == department:
                accepted[department].append(n_applicants.pop(n))
            else:
                n += 1
    return accepted


def admission_list(applicant_list: list):
    for batch in range(COURSE1, COURSE3 + 1):
        ranking_list = get_ranking_list(applicant_list)
        admitted_list = get_admitted(ranking_list, batch)

        candidates = []
        for department in sorted(admitted_list.keys()):
            for persons in admitted_list[department]:
                prs = persons.split()[:SCORE]
                candidates.append(" ".join(prs))

        applicant_list = [student for student in applicant_list if student not in candidates]
    return admitted_list


admitted = admission_list(applicants)

for dept in sorted(admitted.keys()):
    aux_score_col = None
    score = get_course_col(dept)
    if dept in ("Physics", "Biotech", "Engineering"):
        aux_score_col = get_aux_course(dept)
    admitted[dept] = sort_applicants(admitted[dept], score, aux_score_col)
    with open(f"{dept.lower()}.txt", 'w', encoding="utf-8") as f:
        for applicant in admitted[dept]:
            name = applicant.split()[0] + " " + applicant.split()[1]
            if aux_score_col:
                scores = max(
                    float(applicant.split()[ADMISSION_SCORE]),
                    (float(applicant.split()[score]) + float(applicant.split()[aux_score_col])) / 2
                )
            else:
                scores = max(
                    float(applicant.split()[ADMISSION_SCORE]),
                    float(applicant.split()[score])
                )

            f.write(" ".join([name, str(scores)]) + "\n")

