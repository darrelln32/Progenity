public class minHeap 

{
	 Leaf root = null;
	 Leaf next_parent;
	 Leaf lastNode;

	 int count;
	 int current;

	 
	 Leaf [] treez = new Leaf[256];

	 
	// routine to locate a parent in the array

	private int parent(int position)
	{
	  int check;

	  check = position % 2;

	  if (check == 0)
	     return ((position-1)/2);
	  else
	     return (position / 2) ;
	}


	//  swap routine to help create the minHeap
	//  and pushdown elements of the minHeap


	private void swap(int posOne, int posTwo)
	{
	  Leaf temp;

	  temp = treez[posOne];
	  treez[posOne] = treez[posTwo];
	  treez[posTwo] = temp;
	}


	//  determine if the element is a child or a parent

	private boolean isChild(int pos)
	{
	  return ((pos >= count/2) && (pos <= count));
	}


	// find the left child of the element

	 private int leftchild(int pos)
	 {
	  return (2*pos)+1;
	 }




	//  this routine will add a new leaf to the min heap

	public void addLeaf(Leaf leaf)
	{

	  treez[count] = leaf;

	  count++;
	  current = count - 1;
	  
	//  will compare current node to this node and swap
	//  so that the lowest value will be the parent

	 if (count > 1)
	 {
	  while (treez[current].value < treez[parent(current)].value)
	    {
	    swap(current, parent(current));
	    current = parent(current);
	    }
	 }

	}



	// this routine will remove an element from the minHeap

	public Leaf removeMin()
	{

	Leaf minLeaf = null;

	minLeaf = treez[0];
	treez[0] = treez[count-1];

	count--;

	if (count != 0)
	    pushdown(0);


	return minLeaf;
	    

	}


	//  this routine will pushdown the higher element to the bottom of the minHeap

	private void pushdown(int position)
	{
	   int smallChild;

	   //  while the element is a parent
	   //  complare to find the small child, swap and pushdown
	   //  the large child

	   while (!isChild(position))
	   {
	     smallChild = leftchild(position);
	     if ((smallChild < count) && (treez[smallChild].value > treez[smallChild+1].value))
	       smallChild = smallChild + 1;


	     if (treez[position].value <= treez[smallChild].value)
	          return;

	       swap(position,smallChild);
	       position = smallChild;
	   }
	}



}
