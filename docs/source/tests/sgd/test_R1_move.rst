Reidemeister 1 Move
=============

This section documents tests for the R1 move functionality.

.. image:: images/Reidemeister_moves.jpg
   :alt: Test result explanation
   :align: center
   :width: 500px

Examples where no R1 moves are possible

.. image:: images/unknot_1e_1v_0c.jpg
   :alt: Test result explanation
   :align: center
   :width: 500px

.. literalinclude:: ../../../../tests/test_sgd/test_R1_move.py
   :language: python
   :lines: 13-16
   :linenos:
   :caption: Example Test Function

.. image:: images/unknot_2e_2v_0c.jpg
   :alt: Test result explanation
   :align: center
   :width: 500px

.. literalinclude:: ../../../../tests/test_sgd/test_R1_move.py
   :language: python
   :lines: 19-22
   :linenos:
   :caption: Example Test Function

Examples where one R1 move is possible.

.. image:: images/r1_double_loop_same_orientation.jpg
   :alt: Test result explanation
   :align: center
   :width: 500px

.. literalinclude:: ../../../../tests/test_sgd/test_R1_move.py
   :language: python
   :lines: 62-112
   :linenos:
   :caption: Example Test Function

.. image:: images/r1_double_loop_opposite_orientation.jpg
   :alt: Test result explanation
   :align: center
   :width: 500px

.. literalinclude:: ../../../../tests/test_sgd/test_R1_move.py
   :language: python
   :lines: 115-165
   :linenos:
   :caption: Example Test Function

Examples where two R1 moves are possible.