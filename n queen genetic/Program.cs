using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace n_queen_genetic
{
    class Program
    {
        static int n;

        static bool Allowed(ref bool[,] board, int x, int y)
        {
            for (int i = 0; i <= x; i++)
            {
                if (board[i, y] || (i <= y && board[x - i, y - i]) || (y + i < n && board[x - i, y + i]))
                    return false;
            }
            return true;
        }

        static bool Find_Solution(ref bool[,] board, int x)
        {
            for (int i = 0; i < n; i++)
            {
                if (Allowed(ref board, x, i))
                {
                    board[x, i] = true;
                    if (x == n - 1 || Find_Solution(ref board, x + 1)) return true;
                    board[x, i] = false;
                }
            }
            return false;
        }

        static void Main(string[] args)
        {
            Console.Write("Enter number of queens :");
            n = int.Parse(Console.ReadLine());
            bool[,] board = new bool[n, n];


            if (Find_Solution(ref board, 0))
            {
                for (int i = 0; i < n; i++)
                {
                    for (int j = 0; j < n; j++)
                    {
                        Console.Write(board[i, j] ? " X " : " . ");
                    }
                    Console.WriteLine("");
                }
                Console.WriteLine("\n");
                Console.WriteLine("solved");

            }
            else
                Console.WriteLine("No solution found for n = " + n + ".");
            Console.ReadKey();
        }
    }
}

