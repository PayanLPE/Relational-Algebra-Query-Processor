# Relation Algebra Query Processor

Relation Algebra Query Processor is a python file that takes in data and query to perform relational algebra and output the result to terminal. 

## Credits
Author: Peien Liu
Student Number: 101221020

## Usage
1. Download the `RelationAlgebraQueryProcessor.zip` and unzip it. 

2. Edit `data.txt` to import **Relations**, make sure the relation name is followed by '='. Example:
    ```
    Student = 
    {
    id, name, email
    1, 'Alex', 'alex@carleton.ca'
    2, 'John', 'john@carleton.ca'
    3, 'Mo', 'mo@carleton.ca'
    }
    ```

3. Edit `query.txt` to import **Query**, make sure space is provided between brackets and operators/relations. Example:
    ```
    # Selection, condtions MUST be seperated with `,`; no space is needed
    sigma id<3,name=='Alex' ( A )

    # Projection
    pi id,name ( A )

    # Natural Join
    natural_join ( A ) ( B )

    # Left Outer Join
    left_outer_join  ( A ) ( B )

    # Right Outer Join
    right_outer_join  ( A ) ( B )
    
    # Full Outer Join
    full_outer_join  ( A ) ( B )

    # greater than
    >

    # lesser than
    <

    # greater or equal to
    >=

    # lesser or equal to
    <=

    # equal to
    ==

    # not equal to
    !=
    ```
    **NOTE: All relations MUST enclosed by brackets, all brackets MUST have spaces around it. ONLY THE FIRST LINE OF QUERY WILL BE EXECUTED** 

4. Run `RelationAlgebraQueryProcessor.py` using python, the output of relation algebra will be printed on terminal
    ```
    $ python RelationAlgebraQueryProcessor.py
    ```