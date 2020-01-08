#include "func.h"
#include <stdio.h>
#include <string.h>
int square( int a)
{
    return a*a;
}
Point* usePointTest (double x, double y, Point *p)
{
    p->x=x;
    p->y=y;
    printf("In C, point p's x=%.2f, y=%.2f\n", p->x, p->y);
    return p;
}
Point printPointTest(Point p)
{
    printf("In C, before change, point p's x=%.2f, y=%.2f\n", p.x, p.y);
    p.x+=3;
    p.y-=2;
    printf("In C, After change, point p's x=%.2f, y=%.2f\n", p.x, p.y);
    return p;
}
Student* useStudentTest(Student* s,char* name, const int age,const Point* p)
{
    printf("In C, before change, student s's name=%s, age=%d, ", s->name, s->age);
    printf("position=(%.2f, %.2f)\n", s->position.x, s->position.y);
    //strcpy(s->name,name);
    s->name=name;
    s->age=age;
    s->position= *p;
    printf("In C, after change, student s's name=%s, age=%d, ", s->name, s->age);
    printf("position=(%.2f, %.2f)\n", s->position.x, s->position.y);
    return s;
}