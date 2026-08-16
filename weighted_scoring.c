/*
 * Weighted Scoring Toolkit
 * =========================
 * A small command-line toolkit that applies weighted-average scoring
 * to three different scenarios, all built on one reusable core
 * function:
 *
 *   1. Employee performance evaluation (Productivity, Attendance, Teamwork)
 *   2. Weather severity analysis        (Temperature, Humidity, Wind Speed)
 *   3. Student scholarship eligibility  (Math, Science, English)
 *
 * Each mode reads n records of 3 numeric fields, computes a weighted
 * average per record using a mode-specific weight vector, and reports
 * a summary (top performer / most extreme city / eligible students).
 *
 * Compile:  gcc -Wall -o weighted_scoring weighted_scoring.c
 * Run:      ./weighted_scoring
 */

#include <stdio.h>

#define MAX_RECORDS 50
#define NUM_FIELDS 3

typedef struct {
    char label[32];
    float fields[NUM_FIELDS];
    float weighted_score;
} Record;

/* Reusable weighted-average calculation used by every mode. */
float weighted_average(const float fields[NUM_FIELDS], const float weights[NUM_FIELDS]) {
    float total = 0.0f;
    for (int i = 0; i < NUM_FIELDS; i++) {
        total += fields[i] * weights[i];
    }
    return total;
}

/* Reads n records with a given prompt/field description, computes
 * weighted scores, and returns the index of the highest-scoring
 * record (by weighted_score, unless use_field is >= 0, in which case
 * it ranks by that raw field instead — used for "most extreme wind
 * speed" rather than the blended score). */
int collect_and_score(Record records[], int n, const char *record_name,
                       const char *field_names[NUM_FIELDS], const float weights[NUM_FIELDS],
                       int use_field) {
    int top_index = 0;

    for (int i = 0; i < n; i++) {
        printf("\nEnter %s %d - %s: ", record_name, i + 1, field_names[0]);
        scanf("%f", &records[i].fields[0]);
        printf("Enter %s %d - %s: ", record_name, i + 1, field_names[1]);
        scanf("%f", &records[i].fields[1]);
        printf("Enter %s %d - %s: ", record_name, i + 1, field_names[2]);
        scanf("%f", &records[i].fields[2]);

        records[i].weighted_score = weighted_average(records[i].fields, weights);

        float rank_value = (use_field >= 0) ? records[i].fields[use_field] : records[i].weighted_score;
        float top_rank_value = (use_field >= 0) ? records[top_index].fields[use_field]
                                                  : records[top_index].weighted_score;
        if (rank_value > top_rank_value) {
            top_index = i;
        }
    }
    return top_index;
}

void run_employee_evaluation(void) {
    int n;
    printf("Enter number of employees: ");
    scanf("%d", &n);
    if (n <= 0 || n > MAX_RECORDS) { printf("Invalid number of employees.\n"); return; }

    Record employees[MAX_RECORDS];
    const float weights[NUM_FIELDS] = {0.5f, 0.3f, 0.2f};
    const char *fields[NUM_FIELDS] = {"Productivity", "Attendance", "Teamwork"};

    int top = collect_and_score(employees, n, "Employee", fields, weights, -1);

    printf("\n--- Results ---\n");
    for (int i = 0; i < n; i++) {
        printf("Employee %d - Weighted Score: %.2f\n", i + 1, employees[i].weighted_score);
    }
    printf("\nTop-Performing Employee: Employee %d (Score: %.2f)\n",
           top + 1, employees[top].weighted_score);
}

void run_weather_analysis(void) {
    int n;
    printf("Enter number of cities: ");
    scanf("%d", &n);
    if (n <= 0 || n > MAX_RECORDS) { printf("Invalid number of cities.\n"); return; }

    Record cities[MAX_RECORDS];
    const float weights[NUM_FIELDS] = {0.4f, 0.3f, 0.3f};
    const char *fields[NUM_FIELDS] = {"Temperature", "Humidity", "Wind Speed"};

    /* Rank by raw wind speed (field index 2), not the blended score,
     * since "most extreme weather" is defined by wind speed here. */
    int extreme = collect_and_score(cities, n, "City", fields, weights, 2);

    printf("\n--- Results ---\n");
    for (int i = 0; i < n; i++) {
        printf("City %d - Average Weather Score: %.2f\n", i + 1, cities[i].weighted_score);
    }
    printf("\nCity with Most Extreme Weather (Highest Wind Speed): City %d\n", extreme + 1);
}

void run_scholarship_check(void) {
    int n;
    const float cutoff = 90.0f;
    printf("Enter number of students: ");
    scanf("%d", &n);
    if (n <= 0 || n > MAX_RECORDS) { printf("Invalid number of students.\n"); return; }

    Record students[MAX_RECORDS];
    const float weights[NUM_FIELDS] = {0.5f, 0.3f, 0.2f};
    const char *fields[NUM_FIELDS] = {"Math", "Science", "English"};

    collect_and_score(students, n, "Student", fields, weights, -1);

    printf("\n--- Scholarship-Eligible Students (score > %.0f) ---\n", cutoff);
    int any_eligible = 0;
    for (int i = 0; i < n; i++) {
        if (students[i].weighted_score > cutoff) {
            printf("Student %d - Weighted Score: %.2f (Eligible)\n", i + 1, students[i].weighted_score);
            any_eligible = 1;
        }
    }
    if (!any_eligible) {
        printf("No students met the eligibility cutoff.\n");
    }
}

int main(void) {
    int choice;

    printf("Weighted Scoring Toolkit\n");
    printf("1. Employee Performance Evaluation\n");
    printf("2. Weather Severity Analysis\n");
    printf("3. Scholarship Eligibility Check\n");
    printf("Choose a mode (1-3): ");
    scanf("%d", &choice);

    switch (choice) {
        case 1: run_employee_evaluation(); break;
        case 2: run_weather_analysis(); break;
        case 3: run_scholarship_check(); break;
        default: printf("Invalid choice.\n");
    }

    return 0;
}
