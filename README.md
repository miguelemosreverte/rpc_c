# rpc_c
###### A framework to deploy RPC using the tool RPCGEN from Sun Microsystems .

The following configuration of Automator/data_injection.yaml automates two things:

- First it creates a working RPC directory following the commands listed below
- Secondly it also creates a suite of tests using the CUnit library. To avoid boilerplate writing the tests are listed below for them to be injected later onto the actual file.


```
rpcgen:
    - rpcgen -C filename
    - rpcgen -a -C filename
    - mv Makefile.filename_without_extension makefile
    - make
    - sudo systemctl add-wants multi-user.target rpcbind

cunit:
  inject_tests_here: /* Insert your tests here */
  insert_assertions_here: "/* Add the tests to the suite here: Use the following line as template*/"
  tests:
    testClient: |
        /* Simple test of the RPC client*/
        void testClient(void)
        {
          char * output = executeCmd("../add_client localhost");
          CU_ASSERT(strcmp(output, "resultado = 145\n") == 0);
        }

```
