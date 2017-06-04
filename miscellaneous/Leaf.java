public class Leaf
{
	
	   public int         value;
	   public char        content;
	   public Leaf    left;
	   public Leaf    right;
	   public String path = "";
	   
       
	     //    this is the charFreq routine for adding an element
	     //    to the minHeap

	        public Leaf(char content, int value)
	        {
	          this.content  = content;
	          this.value    = value;
	        }

	    //    this charFreq routine adds the two removed nodes from the minHeap


	        public Leaf(Leaf left, Leaf right)
	        {

	    //   assume the left tree is always the one that is lowest

	          this.content  = (left.content < right.content) ? left.content : right.content;
	          this.value    = left.value + right.value;
	          this.left     = left;
	          this.right    = right;

	        }


}
