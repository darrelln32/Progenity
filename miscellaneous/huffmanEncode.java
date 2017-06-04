/**
 * darrell nabors en.605.421.31
 * foundations of algorithms Howework 4 and 5 (Huffman Encoding/Decoding)
 *
 *  
 *
 * @author darrell32
 */





import java.io.*;
import java.util.*;

public class huffmanEncode 
{
	
	/**
	 * @param args
	 */
	
/*  This is the main class for the Huffman encoding/decoding program.  It will
 *   take a user's choice of a text file and convert it to a string of characters.
 *   The program will then pass the string to a routine called processFile.  From there
 *   the string of characters will get encoded and decoded. This routine and the encoding
 *   routine are from a previous program that was written for the Data Structures class.
 *   	
 */
	
	public static void main(String[] args) throws IOException
	{
		FileInputStream fin;
	      DataInputStream read;
	      StringBuffer fileContents;


	      String again = null;
	      String FileName = "";

	      int FileFound = 1;

	      Scanner in = new Scanner(System.in);

	System.out.println("This program evaluates the characters of a file (alphabet)");
	System.out.println("and creates a Huffman encoding algorithm for the letters");
	System.out.println();

	do
	{

	// This section of the program allows the user to type in the
	// name of the file

	System.out.println("Type the name of the file that ");
	System.out.print("contains the expression and press ENTER >>");
	InputStreamReader input = new InputStreamReader(System.in);
	BufferedReader reader = new BufferedReader(input);
	FileName = reader.readLine();


	try
	  {
	    // open the file

	    fin = new FileInputStream (FileName);
	    read = new DataInputStream(fin);
	    fileContents = new StringBuffer();

	    String line = null;

	    while ((line = read.readLine()) != null)
	         fileContents.append("\n").append(line);


	  // call the process file routine which will build the frequency table
	  // and the Huffman Tree

	       processFile(fileContents.toString());


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
	   System.out.print("Do you wish to evaluate another expression [Y/N]? >>");
	 }

	 // read in Y or y character

	    again = in.nextLine();
	    System.out.println();

	}
	    while (again.equalsIgnoreCase("y"));


	}

	
	/** ********************************************************************************************* 
	 ** This is the processFile routine.  it will take the string of characters and build a huffman
	 *  tree.  Once the tree is built, it call the encodeFile and decodeFile routines
    /** ********************************************************************************************* */	

	  private static void processFile(String fileContents)
	        {

	          int[] frequency = new int[256];
	          String huffCode[] = new String[256];
	          int fileChar = 0;
	          int i;
	          int xCount = 0;
	          minHeap newLeaf = new minHeap();
	          Leaf newNode = null;
	          Leaf leaf1 = null;
	          Leaf leaf2 = null;
	          Leaf mergeNode = null;
	          Leaf lastLeaf = null;
	                    

	          // Build the frequency table for each letter

	                for ( i=0; i<fileContents.length(); i++)
	                {
	                 fileChar = (int)fileContents.charAt(i);
	                 frequency[fileChar] = frequency[fileChar] + 1;
	                }
	                
	                	                
	           //  create the leaves for the minHeap
	           //  let newNode equal a new Leaf element to store in the
	           //  minHeap
	                
	                for ( i=0; i<frequency.length; i++)
	                {
	                   if (frequency[i] > 0)
	                   {
	                     newNode = new Leaf((char)(i), frequency[i]);
	                     newLeaf.addLeaf(newNode);
	                     xCount++;
	                   }
	                }   
	                
	       
	           //  Create the Huffman Tree
	           //  let mergeNode equal the added node of the two removed nodes 
	           //  from the minHeap.  Add mergeNode back to the minHeap


	              while (xCount > 1)
	                {
	                 leaf1 = newLeaf.removeMin();
	                 leaf2 = newLeaf.removeMin();
	                 mergeNode = new Leaf(leaf1, leaf2);
	                 newLeaf.addLeaf(mergeNode);
	                 xCount--;
	                }


	              // print a couple of blank lines before printing out the tree
	        
	              System.out.println();
	              System.out.println();
	              

	             //  print out the Huffman encoding algorithm for the expression
	             //  and return the an array of 256 characters called huffCode

	              if (xCount > 0)
	               {
	                 System.out.println("The Huffman encoding for your expression is printed below");
	                 System.out.println();
	                 lastLeaf = newLeaf.removeMin();
	                 huffCode = printTree(lastLeaf);
	                 
	            //  write the .huf file
	                 
	                 encodeFile(fileContents, huffCode);
	                 
	           // decode the .huf file    
	                 
	                 decodeFile(lastLeaf);
	                 
	               }
	              else
	                System.out.println("The file had no elements or did not contain valid characters");

	}
	  
	    /** ********************************************************************************************* 
		 ** This is the encodeFile routine.  It takes the huffCode array and the string of the incoming
		 *  file and writes out the code to a file.  this will be the encoded file of the original text
		 *  file.
	    /** ********************************************************************************************* */	
	  
	  
	  private static void encodeFile(String fileContents, String[] huffCode)  
      {   
    	  int fileChar;
    	  FileOutputStream fileOut; 
    	 
    	  try
  		  {
  		    // Open an output stream
  			fileOut = new FileOutputStream ("nabors.huf");
  			
           // search the array and write out the huffman
  		   // codes to the file	
  			for (int i=0;i<fileContents.length(); i++)
  	       { 
  	         fileChar = (int)fileContents.charAt(i);
  			 new PrintStream(fileOut).print (huffCode[fileChar]);
		   }
  			
  		    // Close our output stream
  		    fileOut.close();
  		 }
  		   // Catches any error conditions
  		catch (IOException e)
  		{
  			System.err.println ("Unable to write to file");
  			System.exit(-1);
  		}
    	  
    	  
    	  
      }  
	  
	  /** ********************************************************************************************* 
		 ** This is the decodeFile routine. It takes the Huffman encoded file and decodes the Huffman 
		 *  codes and translates them to text by calling a decode file routine.  Its call the 
		 *  writeDecodeFile to print out the translated characters  
	    /** ********************************************************************************************* */
	  
	  private static void decodeFile(Leaf lastLeaf)  
      {  
		  FileInputStream fileIn;
	      DataInputStream read;
	      StringBuffer DecodeFileContents = null;
	      String result;
	      

        try
        {
	       fileIn = new FileInputStream ("nabors.huf");
		    read = new DataInputStream(fileIn);
		    DecodeFileContents = new StringBuffer();

		    String line = null;

		    
		    
//		    while (read.available() != 0) read.readLine();
		    
		    	    while ((line = read.readLine()) != null)
            		         DecodeFileContents.append(line);
		    	    
	    
        }     
	   catch (IOException e)
	   {
 			System.err.println ("Unable to read to file");
 			System.exit(-1);
 		}
	   
	   // pass the Huffman tree and the file contents
	   // to decode to translate the huffman encoded
	   // file 
	   result = decode(DecodeFileContents.toString(), lastLeaf);
	   
	   // write the translated characters to the file
	   writeDecodeFile(result);
	   

      }  
	     
	  /** ********************************************************************************************* 
	      this routine will decode the huffman file! this is the code from the HuffmanCodingAmination.java file
          provided by Dr. Benjamin Rodriguez.  it searches the huffman tree and the characters to the
          string.  it will pass the string back to the decodeFile routine 
	  /** ********************************************************************************************* */
	    
	  
       private static String decode(String fileContents, Leaf root) 
       {
         String result = "";
         
        Leaf tree = root; // Start from the root
         
         for (int i = 0; i < fileContents.length(); i++) 
         {
       	  if (fileContents.charAt(i) == '0') 
             tree = tree.left;
           else if (fileContents.charAt(i) == '1')
             tree = tree.right;
           else
             return null; // Wrong bits
           
           if (tree.left == null)
           { // A leaf detected
             result += tree.content;
             tree = root;
              // Restart from the root
           }
         }
         
         return result;
         
         
       }	  
	  
       /** ********************************************************************************************* 
           This routine write the translated string from the decodeFile routine to a file
 	   /** ********************************************************************************************* */ 
       
       private static void writeDecodeFile(String result)  
       {   
     	  char fileChar;
     	  FileOutputStream fileOut; 
     	 
     	  try
   		  {
   		    // Open an output stream
   			fileOut = new FileOutputStream ("naborsDecompressed.txt");
   			

   			for (int i=0;i<result.length(); i++)
   	       { 
   	         fileChar = result.charAt(i);
   			 new PrintStream(fileOut).print(fileChar);
 		   }
   			
   		    // Close our output stream
   		    fileOut.close();
   		 }
   		// Catches any error conditions
   		catch (IOException e)
   		{
   			System.err.println ("Unable to write to file");
   			System.exit(-1);
   		}
     	  
     	  
     	  
       }       
       
       /** ********************************************************************************************* 
           these routines will find the path of the Huffman tree
           and print out the path which will be the huffman
           encoding for the expression
 	   /** ********************************************************************************************* */
       
  
       
       
       private static String[] printTree(Leaf tree)
       {
         String codez[]= new String[256];
        	
         printLeaf(tree,codez);
         return codez;
         
       }   
       
    
       //  modifying routine to write to an array
       
       private static void printLeaf(Leaf tree, String[] codez)
       {
        
               if ((tree.left==null) && (tree.right==null))
               {
                System.out.println(tree.content + " = "+(int)tree.content+" = " + tree.path);
                codez[(int)tree.content] = tree.path;
        	    }
               
               if (tree.left != null)
               {
            	tree.left.path = tree.path + '0';  
            	printLeaf(tree.left, codez);
               }
            	   
               if (tree.right != null)
               {	
            	tree.right.path = tree.path + '1';  
               	printLeaf(tree.right, codez);    
               }
                  
                        
       } 
       
       
       
	  

}
