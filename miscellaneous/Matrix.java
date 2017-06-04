
import java.util.StringTokenizer;

public class Matrix
{
	// this is the Elementz method.  it will take the string array (rowz)
	// from the main program and convert that array into an integer matrix

	  public int[][] Elementz(String[]rowz,int Row)
	  {
	      
	      int Col = 0;
	      int i, j;
	      int r = 0;
	      StringTokenizer PullRowz;


	  // Set column equal to the number of rows to initialize
	  // integer matrix

	      Col = Row;

	      int[][] NewMatrix = new int[Row][Col];

	  // build the integer matrix

	       i=0;
	       j=0;

	       for(r=0;r<rowz.length;r++)
	         {
	           PullRowz = new StringTokenizer(rowz[r]);
	            for(j=0;j<Col;j++)
	             {
	               NewMatrix[i][j] = Integer.parseInt(PullRowz.nextToken());
	             }
	                 i++;
	         }

	  //  return the integer matrix

	      return NewMatrix;


	  }

	// this is the determinant method.  it receives the integer matrix
	// and calculates the determinant


	public int Determinant(int[][]a ,int order)
	{
	  int detA = 0;

	  int r, c, i, j, x;

	  // let b equal the new matrix.  set the the dimensions of the matrix
	  // to order+1 to prevent and outof bounds exception error

	  int[][] b = new int[order+1][order+1];

	//  the base case of the matrix

	  if (order == 2)
	  {
	     detA =  ((a[0][0]*a[1][1]) - (a[0][1]*a[1][0]));
	     return detA;
	  }

	//  build the matrix when the order is greater than two

	 for(x=0;x<order;x++)
	   {
	     // i and j will be the index of the row and column of the new matrix
	     // r and c will be the index of the row and column of matrix a

	     i=0;
	     j=0;

	     //  start @ the first row of matrix a and build the determinant matrix
	    
	     for(r=1;r<order;r++)
	     {
	        for(c=0;c<order;c++)
	        {
	           if(c==x)
	             continue;
	           b[i][j] = a[r][c];
	           j++;
	           if(j==(order-1))
	           {
	               i++;
	               j=0;
	           }

	        }
	     }

	// recursive call for the determinant

	detA = (int) (detA + a[0][x]*Math.pow(-1,x)*Determinant(b,order-1));

	   }
	return detA;
	}



}
