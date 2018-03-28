//for a better representation of the variables, see https://en.wikipedia.org/wiki/Triangle#/media/File:Triangle_with_notations_2.svg
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TriangleInfo
{
    class Program
    {
        static bool IsThisTriangle(double x1, double y1, double x2, double y2, double x3, double y3)
        {
            //if the points are on a line that is perpendicular/parallel to the axis lines
            if ((x1 == x2) && (x2 == x3) || (y1 == y2) && (y2 == y3))
            {
                return false;
            }
            //else if the points are on a line that is not perpendicular/parallel to any of the axis lines
            else if ((x1 - x2) / (x3 - x2) == (y1 - y2) / (y3 - y2))
            {
                return false;
            }
            //else it is a triangle
            else
            {
                return true;
            }
        }
        static double LineSegmentLength(double x1, double y1, double x2, double y2)
        {
            //a = ((x1 - x2)^2 + (y1 - y2)^2)^0.5
            return Math.Pow(Math.Pow(x1 - x2, 2.0) + Math.Pow(y1 - y2, 2.0), 0.5);
        }
        static double TriangleArea(double angleA,double b,double c)
        {
            //S = a*b*sin(a)/2
            return b*c*Math.Sin(angleA / 180*Math.PI)/2;
        }
        static double TrianglePerimeter(double a,double b,double c)
        {
            //P = a+b+c
            return a+b+c;
        }
        static double GetAngleD(double a,double b,double c)
        {
            //returns angle in degrees that is opposite of the first given line segment length
            //cos(A) = (b^2 + c^2 - a^2)/(2*b*c)
            return Math.Acos((b*b + c*c - a*a) / (2*b*c)) * 180/Math.PI;
        }
        static double GetAngleR(double a,double b,double c)
        {
            //the same as GetAngleD, but in radians
            return Math.Acos((b*b + c*c - a*a) / (2*b*c));
        }
        static double DegtoRad(double deg)
        {
            //converts degrees to radians
            return deg*Math.PI/180;
        }
        static double RadtoDeg(double rad)
        {
            //converts radians to degrees
            return rad*180/Math.PI;
        }
        static int TriangleTypeSides(double a, double b, double c)
        {
            //(a-b <= EPSILON) is made because a == b sometimes doesn't return true with doubles (e.g. 5*Math.Pow(3,0.5) and 8.66025403784439)
            double EPSILON = 0.00000000000001;
            //Equilateral Triangle
            if ((Math.Abs(a - b) < EPSILON) && (Math.Abs(b - c) < EPSILON))
            {
                return 0;
            }
            //Isosceles Triangle
            else if (((Math.Abs(a - b) <= EPSILON) && (b != c)) || ((Math.Abs(a - c) <= EPSILON) && (b != c)) || ((Math.Abs(b - c) <= EPSILON) && (a != c)))
            {
                return 1;
            }
            //Scalene Triangle
            else
            {
                return 2;
            }
        }
        static int TriangleTypeAngels(double angle1, double angle2, double angle3)
        {
            //Right Triangle
            if (angle1 == 90 || angle2 == 90 || angle3 == 90)
            {
                return 0;
            }
            //Obtuse Triangle
            else if (angle1 > 90 || angle2 > 90 || angle3 > 90)
            {
                return 1;
            }
            //Acute Triangle
            else
            {
                return 2;
            }
        }
        static void PrintTriangleInfo(double x1, double y1, double x2, double y2, double x3, double y3)
        {
            Console.WriteLine("Coordinates:");
            Console.WriteLine("("+x1+"; "+y1+")("+x2+"; "+y2+")("+x3+"; "+y3+")\n");
            if (IsThisTriangle(x1, y1, x2, y2, x3, y3))
            {
                Console.WriteLine("It is a triangle.");
                Console.Write("Lengths of the sides: ");
                double a = LineSegmentLength(x1, y1, x2, y2);
                double b = LineSegmentLength(x2, y2, x3, y3);
                double c = LineSegmentLength(x1, y1, x3, y3);
                Console.Write(a + " ");
                Console.Write(b + " ");
                Console.WriteLine(c);
                string[] triangletypessides = {"equilateral", "isosceles", "scalene"};
                Console.WriteLine("This triangle is "+ triangletypessides[TriangleTypeSides(a, b, c)]);
                double angleA = GetAngleD(a,b,c);
                double angleB = GetAngleD(b,a,c);
                double angleC = GetAngleD(c,a,b);
                Console.Write("Angles: ");
                Console.Write(angleA+"° ("+DegtoRad(angleA)+") ");
                Console.Write(angleB+"° ("+DegtoRad(angleB)+") ");
                Console.WriteLine(angleC+"° ("+DegtoRad(angleC)+")");
                string[] triangletypesangles = { "right", "obtuse", "acute" };
                Console.WriteLine("This triangle is "+triangletypesangles[TriangleTypeAngels(angleA, angleB, angleC)]);
                Console.WriteLine("Area: "+TriangleArea(angleA,b,c));
                Console.WriteLine("Perimeter: "+TrianglePerimeter(a,b,c));
            }
            else
            {
                Console.WriteLine("It is not a triangle.");
            }
        }
        static void Main(string[] args)
        {
            Random rand = new Random();
            string[] triangletypes = { "right","obtuse","acute","isosceles","scalene" };
            string[] triangletypessides = {"isosceles","scalene" };
            string[] triangletypesangles = { "right","obtuse","acute" };
            while (true)
            {
                double x1 = 0, y1 = 0, x2 = 0, y2 = 0, x3 = 0, y3 = 0;
                Console.WriteLine("Enter coordinates of your triangle in this order: x1 y1 x2 y2 x3 y3.\nIf you want to generate a random triangle, enter \"random\". For more specific random triangles, enter \"isosceles\", \"scalene\", \"right\", \"obtuse\", or \"acute\" after \"random\".");
                string user_input = Console.ReadLine().ToLower();
                string[] user_input_list = user_input.Split(new char[] {' '},StringSplitOptions.RemoveEmptyEntries);
                string triangle = "null";
                if (user_input_list.Length != 0)
                {
                    Console.WriteLine("\n");
                    if (user_input_list[0] == "random")
                    {
                        if (user_input_list.Length == 1)
                        {
                            triangle = "random";
                        }
                        else if (triangletypes.Contains(user_input_list[1]))
                        {
                            triangle = user_input_list[1];
                        }
                    }
                    else if (user_input_list.Length == 6)
                    {
                        try
                        {
                            x1 = Convert.ToDouble(user_input_list[0]);   //1st point's X
                            y1 = Convert.ToDouble(user_input_list[1]);   //1st point's Y
                            x2 = Convert.ToDouble(user_input_list[2]);   //2nd point's X
                            y2 = Convert.ToDouble(user_input_list[3]);   //2st point's Y
                            x3 = Convert.ToDouble(user_input_list[4]);   //3rd point's X
                            y3 = Convert.ToDouble(user_input_list[5]);   //3rd point's Y
                            triangle = "user";
                        }
                        catch { }
                    }
                    if (triangletypes.Contains(triangle) || triangle == "random")
                    {
                        while (true)
                        {
                            x1 = rand.Next(-100,101);      //1st point's X
                            y1 = rand.Next(-100,101);      //1st point's Y
                            x2 = rand.Next(-100,101);      //2nd point's X
                            y2 = rand.Next(-100,101);      //2st point's Y
                            x3 = rand.Next(-100,101);      //3rd point's X
                            y3 = rand.Next(-100,101);      //3rd point's Y
                            if (IsThisTriangle(x1,y1,x2,y2,x3,y3))
                            {
                                if (triangle == "random")
                                {
                                    break;
                                }
                                double a = LineSegmentLength(x1,y1,x2,y2);
                                double b = LineSegmentLength(x2,y2,x3,y3);
                                double c = LineSegmentLength(x1,y1,x3,y3);
                                if (triangletypessides.Contains(triangle))
                                {
                                    if (triangle == triangletypessides[TriangleTypeSides(a,b,c)-1])
                                    {
                                        break;
                                    }
                                }
                                if (triangletypesangles.Contains(triangle))
                                {
                                    double angleA = GetAngleD(a,b,c);
                                    double angleB = GetAngleD(b,a,c);
                                    double angleC = GetAngleD(c,a,b);
                                    if (triangle == triangletypesangles[TriangleTypeAngels(angleA,angleB,angleC)])
                                    {
                                        break;
                                    }
                                }
                            }
                        }
                    }
                    if (triangle != "null")
                    {
                        PrintTriangleInfo(x1,y1,x2,y2,x3,y3);
                    }
                }
                if (triangle == "null")
                {
                    Console.WriteLine("\nWrong Input");
                }
                Console.WriteLine("\n");
            }
        }
    }
}
