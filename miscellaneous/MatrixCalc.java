

import java.io.*;
import java.util.StringTokenizer;
import java.util.Scanner;


public class MatrixCalc 
{

	/**
	 * @param args
	 */
	public static void main(String[] args) throws IOException
	{

	      FileInputStream fin;
	      DataInputStream read;

	      int PrintMatrix = 0;
	      String row_one;
	      String again = null;
	      int Row = 0;
	      int Col = 0;
	      int i, j;
	      int r = 0;
	      int FileFound = 1;
	      int DetOfMatrix = 0;
	      StringTokenizer PullRowCol;
	      
	      Scanner in = new Scanner(System.in);

	do
	{

	// This section of the program allows the user to type in the
	// name of the file

	System.out.println("Type the name of the file that ");
	System.out.print("contains the matrix and press Enter >>");
	String FileName = "";
	InputStreamReader input = new InputStreamReader(System.in);
	BufferedReader reader = new BufferedReader(input);
	FileName = reader.readLine();


	//   assign CalcMatrix variable to class Matrix

	     Matrix CalcMatrix = new Matrix();


	//  The "foundfile" label will allow the program to break out of the
	//  program while in the try/catch loop for the file but it will still
	//  allow the user to continue the program.  the first try/catch loop
	//  throws an exception if it cannot find the file


	foundfile:
	try
	  {
	    // open the file

	    fin = new FileInputStream (FileName);
	    read = new DataInputStream(fin);

	    // read the top line line of file for # of Rows and Columns

	    row_one = read.readLine();

	    PullRowCol = new StringTokenizer(row_one);

	//  this try/catch will alert the user if the row or column
	//  number is not an integer

	try
	{
	    Row = Integer.parseInt(PullRowCol.nextToken());
	    Col = Integer.parseInt(PullRowCol.nextToken());

	// print out file and number of rows and columns

	    System.out.println();
	    System.out.println("Your matrix file >> " + FileName);
	    System.out.println("Number of Rows = " + Row);
	    System.out.println("Number of Columns = " + Col);
	         
	}
	catch(NumberFormatException nFE)
	{
	    System.err.println("One or both of the numbers in the");
	    System.err.println("Row/Column field is not as integer!");
	    FileFound = 0;
	    break foundfile;
	}

//	    the if statement looks to see if the # of rows and columns
//	    do not match, or if there is a zero or one for either number

	 if ((Row != Col)||(Row <= 1)||(Col <= 1))
	   {
	    System.err.println("There is a problem with the Row and Column line");
	    System.err.println("in your file. Cannot use this file");
	    System.err.println("for Determinant Calculcation");
	    FileFound = 0;
	    break foundfile;
	   }

	//  the program will set a matrix called rowz to receive the string data
	//  from the matrix file

	    String [] rowz = new String[Row];

	    for(r=0;r<rowz.length;r++)
	        rowz[r] = read.readLine();

	    

	//  NewMatrix will be the integer matrix from which the determinant
	//  be calculated.  set the matrix to the # of rows and columns
	//  read in from the matrix file

	    int[][] NewMatrix = new int[Row][Col];

	//  this try/catch will alert the user if any element
	//  of the matrix is not an integer

	try
	{

	//  pass the string matrix and the number of rows to the
	//  matrix class

	  NewMatrix = CalcMatrix.Elementz(rowz,Row);
	}
	catch(NumberFormatException nFE)
	{
	  System.err.println("All of the elements in the file are not integers!");
	  System.err.println("Cannot use this file");
	  System.err.println("for Determinant Calculcation");
	  FileFound = 0;
	  break foundfile;
	}

	// print out integer matrix returned from the matrix class

	   System.out.println();

	   for(i=0;i<Row;i++)
	   {
	      for(j=0;j<Col;j++)
	      {
	         System.out.print(NewMatrix[i][j]);
	         System.out.print(" ");
	      }
	          System.out.println();
	   }


	// calculate the determinant of the matrix

	   DetOfMatrix = CalcMatrix.Determinant(NewMatrix,Row);

	//  print out the determinant

	System.out.println();
	System.out.println("The determinant of "+FileName+" is " + DetOfMatrix);
	  
	// close the file
	    
	    fin.close();

	}

	// catches error for the filename or opening the file
	// (part of the try/catch exception for the file

	    catch (IOException e)
	    {
	      System.out.println();
	      System.err.println ("Sorry cannot find the file " + FileName);
	      System.err.println ("That file may be corrupted");
	      FileFound = 0;
	    }

	//  allows the user to enter the file name again or find
	//  another file without quitting the program
	  
	 if (FileFound == 0)
	   {
	     System.out.println();
	     System.out.print("Do you wish to try another file [Y/N]? >>");
	     FileFound = 1;
	   }
	 else
	 {
	   System.out.println();
	   System.out.print("Do you wish to evaluate another matrix [Y/N]? >>");
	 }
	    
	 // read in Y or y character

	    again = in.nextLine();
	    System.out.println();

	}
	    while (again.equalsIgnoreCase("y"));
	       
	

	}

}
