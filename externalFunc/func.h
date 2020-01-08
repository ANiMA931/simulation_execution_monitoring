#ifndef _FUNC_H_
#define _FUNC_H_
typedef struct point
{
    double x;
    double y;
}Point;
typedef struct student
{
    char* name;
    int age;
    Point position;
}Student;
int square( int a);
Point* usePointTest( double x, double y, Point *p);
Point printPointTest(Point p);
Student* useStudentTest(Student* s,char* name, const int age, const Point *p);
#endif