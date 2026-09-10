<!-- 从 nvshmem-sync.html 迁移的资料快照；原始 HTML SHA-256: 8b909f94895d734d8d7dfa0158576af9ac6abeeff9d39ade056395b9438cbaf4。 -->

- [](../../index.html)
- [NVSHMEM APIs](../../api.html)
- Point-To-Point Synchronization

[Is this page helpful?](https://surveys.hotjar.com/4904bf71-6484-47a7-83ff-4715cceabdb5)

<a id="point-to-point-synchronization"></a>

# Point-To-Point Synchronization
The following section discusses NVSHMEMAPIs that provide a mechanism for synchronization between two PEs based on the value of a symmetric data object. The point-to-point synchronization routines can be used to portably ensure that memory access operations observe remote updates in the order enforced by the initiator PE using the `nvshmem_fence` and `nvshmem_quiet` routines.

The standard AMO types include some of the exact-width integer types defined in `stdint.h` by *C* §7.18.1.1 and *C* §7.20.1.1. When the *C* translation environment does not provide exact-width integer types with `stdint.h`, an NVSHMEM implemementation is not required to provide support for these types. The `nvshmem_test_any` and `nvshmem_wait_until_any` routines require the `SIZE_MAX` macro defined in `stdint.h` by *C* §7.18.3 and *C* §7.20.3.

The point-to-point synchronization interface provides named constants whose values are integer constant expressions that specify the comparison operators used by NVSHMEM synchronization routines. The constant names and associated operations are presented in Table [\[p2p-consts\]](#p2p-consts).

| Constant Name    | Comparison               |
|------------------|--------------------------|
| `NVSHMEM_CMP_EQ` | Equal                    |
| `NVSHMEM_CMP_NE` | Not equal                |
| `NVSHMEM_CMP_GT` | Greater than             |
| `NVSHMEM_CMP_GE` | Greater than or equal to |
| `NVSHMEM_CMP_LT` | Less than                |
| `NVSHMEM_CMP_LE` | Less than or equal to    |

Point-to-Point Comparison Constants[\#](#p2p-consts "Link to this table") {#p2p-consts}

<a id="nvshmem-wait-until"></a>

## **NVSHMEM_WAIT_UNTIL**
void nvshmemx_TYPENAME_wait_until_on_stream(

*TYPE \*ivar*,

*int cmp*,

*TYPE cmp_value*,

*cudaStream_t stream*

)[\#](#c.nvshmemx_TYPENAME_wait_until_on_stream "Link to this definition")  

\_\_device\_\_ void nvshmem_TYPENAME_wait_until(TYPE \*ivar, int cmp, TYPE cmp_value)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

void nvshmemx_TYPENAME_wait_on_stream(

*TYPE \*ivar*,

*TYPE cmp_value*,

*cudaStream_t stream*

)[\#](#c.nvshmemx_TYPENAME_wait_on_stream "Link to this definition")  

\_\_device\_\_ void nvshmem_TYPENAME_wait(TYPE \*ivar, TYPE cmp_value)  
where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

&nbsp;

*ivar \[IN\]*  
Symmetric address of a remotely accessible data object. The type of `ivar` should match that implied in the SYNOPSIS section.

*cmp \[IN\]*  
The compare operator that compares `ivar` with `cmp_value`.

*cmp_value \[IN\]*  
The value to be compared with `ivar`. The type of `cmp_value` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_wait` and `nvshmem_wait_until` operations block until the value contained in the symmetric data object, `ivar`, at the calling PE satisfies the wait condition. The `ivar` object at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE.

These routines can be used to implement point-to-point synchronization between PEs or between threads within the same PE. A call to `nvshmem_wait` blocks until the value of `ivar` at the calling PE is not equal to `cmp_value`. A call to `nvshmem_wait_until` blocks until the value of `ivar` at the calling PE satisfies the wait condition specified by the comparison operator, `cmp`, and comparison value, `cmp_value`.

Implementations must ensure that `nvshmem_wait` and `nvshmem_wait_until` do not return before the update of the memory indicated by `ivar` is fully complete.

**Returns**

None

<a id="nvshmem-wait-until-all"></a>

## **NVSHMEM_WAIT_UNTIL_ALL**
\_\_device\_\_ void nvshmem_TYPENAME_wait_until_all(TYPE \*ivars, size_t nelems, const int \*status, int cmp, TYPE cmp_value)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the wait set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with `cmp_value`.

*cmp_value \[IN\]*  
The value to be compared with the objects pointed to by `ivars`. The type of `cmp_value` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_wait_until_all` routine waits until all entries in the wait set specified by `ivars` and `status` have satisfied the wait condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. If `nelems` is 0, the wait set is empty and this routine returns immediately. This routine compares each element of the `ivars` array in the wait set with the value `cmp_value` according to the comparison operator `cmp` at the calling PE. This routine is semantically similar to `nvshmem_wait_until` in Section [NVSHMEM_WAIT_UNTIL](#subsec-shmem-wait-until), but adds support for point-to-point synchronization involving an array of symmetric data objects.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the wait set. Elements of `status` set to 0 will be included in the wait set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the wait set is empty and this routine returns immediately. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the wait set. The `ivars` and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_wait_until_all` does not return before the update of the memory indicated by `ivars` is fully complete.

**Returns**

None.

The following *C* example demonstrates the use of `nvshmem_wait_until_all` to implement a simple linear barrier synchronization. ./example_code/shmem_wait_until_all.c

<a id="nvshmem-wait-until-any"></a>

## **NVSHMEM_WAIT_UNTIL_ANY**
\_\_device\_\_ size_t nvshmem_TYPENAME_wait_until_any(TYPE \*ivars, size_t nelems, const int \*status, int cmp, TYPE cmp_value)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the wait set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with `cmp_value`.

*cmp_value \[IN\]*  
The value to be compared with the objects pointed to by `ivars`. The type of `cmp_value` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_wait_until_any` routine waits until any one entry in the wait set specified by `ivars` and `status` satisfies the wait condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine compares each element of the `ivars` array in the wait set with the value `cmp_value` according to the comparison operator `cmp` at the calling PE. The order in which these elements are waited upon is unspecified. If an entry \\i\\ in `ivars` within the wait set satisfies the wait condition, a series of calls to `nvshmem_wait_until_any` must eventually return \\i\\.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the wait set. Elements of `status` set to 0 will be included in the wait set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the wait set is empty and this routine returns `SIZE_MAX`. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the wait set. The `ivars` and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_wait_until_any` does not return before the update of the memory indicated by `ivars` is fully complete.

**Returns**

`nvshmem_wait_until_any` returns the index of an element in the `ivars` array that satisfies the wait condition. If the wait set is empty, this routine returns `SIZE_MAX`.

The following *C* example demonstrates the use of `nvshmem_wait_until_any` to process a simple all-to-all transfer of \\N\\ data elements through a sum reduction. ./example_code/shmem_wait_until_any_all2all_sum.c

<a id="nvshmem-wait-until-some"></a>

## **NVSHMEM_WAIT_UNTIL_SOME**
\_\_device\_\_ size_t nvshmem_TYPENAME_wait_until_some(TYPE \*ivars, size_t nelems, size_t \*indices, const int \*status, int cmp, TYPE cmp_value)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*indices \[OUT\]*  
Local address of an array of indices of length at least `nelems` into `ivars` that satisfied the wait condition.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the wait set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with `cmp_value`.

*cmp_value \[IN\]*  
The value to be compared with the objects pointed to by `ivars`. The type of `cmp_value` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_wait_until_some` routine waits until at least one entry in the wait set specified by `ivars` and `status` satisfies the wait condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine compares each element of the `ivars` array in the wait set with the value `cmp_value` according to the comparison operator `cmp` at the calling PE. This routine tests all elements of `ivars` in the wait set at least once, and the order in which the elements are waited upon is unspecified.

Upon return, the `indices` array contains the indices of at least one element in the wait set that satisfied the wait condition during the call to `nvshmem_wait_until_some`. The return value of `nvshmem_wait_until_some` is equal to the total number of these satisfied elements. For a given return value \\N\\, the first \\N\\ elements of the `indices` array contain those unique indices that satisfied the wait condition. These first \\N\\ elements of `indices` may be unordered with respect to the corresponding indices of `ivars`. The array pointed to by `indices` must be at least `nelems` long. If an entry \\i\\ in `ivars` within the wait set satisfies the wait condition, a series of calls to `nvshmem_wait_until_some` must eventually include \\i\\ in the `indices` array.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the wait set. Elements of `status` set to 0 will be included in the wait set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the wait set is empty and this routine returns 0. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the wait set. The `ivars`, `indices`, and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_wait_until_some` does not return before the update of the memory indicated by `ivars` is fully complete.

**Returns**

`nvshmem_wait_until_some` returns the number of indices returned in the `indices` array. If the wait set is empty, this routine returns 0.

The following *C* example demonstrates the use of `nvshmem_wait_until_some` to process a simple all-to-all transfer of \\N\\ data elements through a sum reduction. This pattern is similar to the `nvshmem_wait_until_any` example above, but may reduce the number of iterations in the while loop. ./example_code/shmem_wait_until_some_all2all_sum.c

<a id="nvshmem-wait-until-all-vector"></a>

## **NVSHMEM_WAIT_UNTIL_ALL_VECTOR**
\_\_device\_\_ void nvshmem_TYPENAME_wait_until_all_vector(TYPE \*ivars, size_t nelems, const int \*status, int cmp, TYPE \*cmp_values)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the wait set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with elements of `cmp_values`.

*cmp_values \[IN\]*  
Local address of an array of length `nelems` containing values to be compared with the respective objects in `ivars`. The type of `cmp_values` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_wait_until_all_vector` routine waits until all entries in the wait set specified by `ivars` and `status` have satisfied the wait conditions at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. If `nelems` is 0, the wait set is empty and this routine returns immediately. This routine compares each element of the `ivars` array in the wait set with each respective value in `cmp_values` according to the comparison operator `cmp` at the calling PE.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the wait set. Elements of `status` set to 0 will be included in the wait set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the wait set is empty and this routine returns immediately. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the wait set. The `ivars` and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_wait_until_all_vector` does not return before the update of the memory indicated by `ivars` is fully complete.

**Returns**

None.

<a id="nvshmem-wait-until-any-vector"></a>

## **NVSHMEM_WAIT_UNTIL_ANY_VECTOR**
\_\_device\_\_ size_t nvshmem_TYPENAME_wait_until_any_vector(TYPE \*ivars, size_t nelems, const int \*status, int cmp, TYPE \*cmp_values)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the wait set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with elements of `cmp_values`.

*cmp_values \[IN\]*  
Local address of an array of length `nelems` containing values to be compared with the respective objects in `ivars`. The type of `cmp_values` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_wait_until_any_vector` routine waits until any one entry in the wait set specified by `ivars` and `status` satisfies the wait condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine compares each element of the `ivars` array in the wait set with each respective value in `cmp_values` according to the comparison operator `cmp` at the calling PE. The order in which these elements are waited upon is unspecified. If an entry \\i\\ in `ivars` within the wait set satisfies the wait condition, a series of calls to `nvshmem_wait_until_any_vector` must eventually return \\i\\.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the wait set. Elements of `status` set to 0 will be included in the wait set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the wait set is empty and this routine returns `SIZE_MAX`. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the wait set. The `ivars` and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_wait_until_any_vector` does not return before the update of the memory indicated by `ivars` is fully complete.

**Returns**

`nvshmem_wait_until_any_vector` returns the index of an element in the `ivars` array that satisfies the wait condition. If the wait set is empty, this routine returns `SIZE_MAX`.

The following *C* example demonstrates the use of `nvshmem_wait_until_any_vector` to wait on values that differ between even PEs and odd PEs. ./example_code/shmem_wait_until_any_vector.c

<a id="nvshmem-wait-until-some-vector"></a>

## **NVSHMEM_WAIT_UNTIL_SOME_VECTOR**
\_\_device\_\_ size_t nvshmem_TYPENAME_wait_until_some_vector(TYPE \*ivars, size_t nelems, size_t \*indices, const int \*status, int cmp, TYPE \*cmp_values)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*indices \[OUT\]*  
Local address of an array of indices of length at least `nelems` into `ivars` that satisfied the wait condition.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the wait set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with elements of `cmp_values`.

*cmp_values \[IN\]*  
Local address of an array of length `nelems` containing values to be compared with the respective objects in `ivars`. The type of `cmp_values` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_wait_until_some_vector` routine waits until at least one entry in the wait set specified by `ivars` and `status` satisfies the wait condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine compares each element of the `ivars` array in the wait set with each respective value in `cmp_values` according to the comparison operator `cmp` at the calling PE. This routine tests all elements of `ivars` in the wait set at least once, and the order in which the elements are waited upon is unspecified.

Upon return, the `indices` array contains the indices of at least one element in the wait set that satisfied the wait condition during the call to `nvshmem_wait_until_some_vector`. The return value of `nvshmem_wait_until_some_vector` is equal to the total number of these satisfied elements. For a given return value \\N\\, the first \\N\\ elements of the `indices` array contain those unique indices that satisfied the wait condition. These first \\N\\ elements of `indices` may be unordered with respect to the corresponding indices of `ivars`. The array pointed to by `indices` must be at least `nelems` long. If an entry \\i\\ in `ivars` within the wait set satisfies the wait condition, a series of calls to `nvshmem_wait_until_some_vector` must eventually include \\i\\ in the `indices` array.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the wait set. Elements of `status` set to 0 will be included in the wait set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the wait set is empty and this routine returns 0. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the wait set. The `ivars`, `indices`, and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_wait_until_some_vector` does not return before the update of the memory indicated by `ivars` is fully complete.

**Returns**

`nvshmem_wait_until_some_vector` returns the number of indices returned in the `indices` array. If the wait set is empty, this routine returns 0.

<a id="nvshmem-test"></a>

## **NVSHMEM_TEST**
\_\_device\_\_ int nvshmem_TYPENAME_test(TYPE \*ivar, int cmp, TYPE cmp_value)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivar \[IN\]*  
Symmetric address of a remotely accessible data object. The type of `ivar` should match that implied in the SYNOPSIS section.

*cmp \[IN\]*  
The comparison operator that compares `ivar` with `cmp_value`.

*cmp_value \[IN\]*  
The value against which the object pointed to by `ivar` will be compared. The type of `cmp_value` should match that implied in the SYNOPSIS section.

**Description**

`nvshmem_test` tests the numeric comparison of the symmetric object pointed to by `ivar` with the value `cmp_value` according to the comparison operator `cmp`. The `ivar` object at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE.

Implementations must ensure that `nvshmem_test` does not return 1 before the update of the memory indicated by `ivar` is fully complete.

**Returns**

`nvshmem_test` returns 1 if the comparison of the symmetric object pointed to by `ivar` with the value `cmp_value` according to the comparison operator `cmp` evaluates to true; otherwise, it returns 0.

The following example demonstrates the use of `nvshmem_test` to wait on an array of symmetric objects and return the index of an element that satisfies the specified condition. ./example_code/shmem_test_example1.c

<a id="nvshmem-test-all"></a>

## **NVSHMEM_TEST_ALL**
\_\_device\_\_ int nvshmem_TYPENAME_test_all(TYPE \*ivars, size_t nelems, const int \*status, int cmp, TYPE cmp_value)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the test set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with `cmp_value`.

*cmp_value \[IN\]*  
The value to be compared with the objects pointed to by `ivars`. The type of `cmp_value` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_test_all` routine indicates whether all entries in the test set specified by `ivars` and `status` have satisfied the test condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine does not block and returns zero if not all entries in `ivars` satisfied the test condition. This routine compares each element of the `ivars` array in the test set with the value `cmp_value` according to the comparison operator `cmp` at the calling PE.

If `nelems` is 0, the test set is empty and this routine returns 1.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the test set. Elements of `status` set to 0 will be included in the test set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the test set is empty and this routine returns 0. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the test set. The `ivars`, `indices`, and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_test_all` does not return 1 before the update of the memory indicated by `ivars` is fully complete.

**Returns**

`nvshmem_test_all` returns 1 if all variables in `ivars` satisfy the test condition or if `nelems` is 0, otherwise this routine returns 0.

<a id="nvshmem-test-any"></a>

## **NVSHMEM_TEST_ANY**
\_\_device\_\_ size_t nvshmem_TYPENAME_test_any(TYPE \*ivars, size_t nelems, const int \*status, int cmp, TYPE cmp_value)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the test set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with `cmp_value`.

*cmp_value \[IN\]*  
The value to be compared with the objects pointed to by `ivars`. The type of `cmp_value` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_test_any` routine indicates whether any entry in the test set specified by `ivars` and `status` has satisfied the test condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine does not block and returns `SIZE_MAX` if no entries in `ivars` satisfied the test condition. This routine compares each element of the `ivars` array in the test set with the value `cmp_value` according to the comparison operator `cmp` at the calling PE. The order in which these elements are tested is unspecified. If an entry \\i\\ in `ivars` within the test set satisfies the test condition, a series of calls to `nvshmem_test_any` must eventually return \\i\\.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the test set. Elements of `status` set to 0 will be included in the test set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the test set is empty and this routine returns `SIZE_MAX`. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the test set. The `ivars` and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_test_any` does not return an index before the update of the memory indicated by the corresponding `ivars` element is fully complete.

**Returns**

`nvshmem_test_any` returns the index of an element in the `ivars` array that satisfies the test condition. If the test set is empty or no conditions in the test set are satisfied, this routine returns `SIZE_MAX`.

The following *C* example demonstrates the use of `nvshmem_test_any` to implement a simple linear barrier synchronization while potentially overlapping communication with computation. ./example_code/shmem_test_any_example.c

<a id="nvshmem-test-some"></a>

## **NVSHMEM_TEST_SOME**
\_\_device\_\_ size_t nvshmem_TYPENAME_test_some(TYPE \*ivars, size_t nelems, size_t \*indices, const int \*status, int cmp, TYPE cmp_value)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*indices \[OUT\]*  
Local address of an array of indices of length at least `nelems` into `ivars` that satisfied the test condition.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the test set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with `cmp_value`.

*cmp_value \[IN\]*  
The value to be compared with the objects pointed to by `ivars`. The type of `cmp_value` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_test_some` routine indicates whether at least one entry in the test set specified by `ivars` and `status` satisfies the test condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine does not block and returns zero if no entries in `ivars` satisfied the test condition. This routine compares each element of the `ivars` array in the test set with the value `cmp_value` according to the comparison operator `cmp` at the calling PE. This routine tests all elements of `ivars` in the test set at least once, and the order in which the elements are tested is unspecified. If an entry \\i\\ in `ivars` within the test set satisfies the test condition, a series of calls to `nvshmem_test_some` must eventually return \\i\\.

Upon return, the `indices` array contains the indices of the elements in the test set that satisfied the test condition during the call to `nvshmem_test_some`. The return value of `nvshmem_test_some` is equal to the total number of these satisfied elements. If the return value is \\N\\, then the first \\N\\ elements of the `indices` array contain those unique indices that satisfied the test condition. These first \\N\\ elements of `indices` may be unordered with respect to the corresponding indices of `ivars`. The array pointed to by `indices` must be at least `nelems` long. If an entry \\i\\ in `ivars` within the test set satisfies the test condition, a series of calls to `nvshmem_test_some` must eventually include \\i\\ in the `indices` array.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the test set. Elements of `status` set to 0 will be included in the test set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the test set is empty and this routine returns 0. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the test set. The `ivars`, `indices`, and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_test_some` does not return indices before the updates of the memory indicated by the corresponding `ivars` elements are fully complete.

**Returns**

`nvshmem_test_some` returns the number of indices returned in the `indices` array. If the test set is empty, this routine returns 0.

The following *C* example demonstrates the use of `nvshmem_test_some` to process a simple all-to-all transfer of \\N\\ data elements through a sum reduction, while potentially overlapping communication with computation. This pattern is similar to the `nvshmem_test_any` example above, but each while loop iteration may process more than one data item. ./example_code/shmem_test_some_example.c

<a id="nvshmem-test-all-vector"></a>

## **NVSHMEM_TEST_ALL_VECTOR**
\_\_device\_\_ int nvshmem_TYPENAME_test_all_vector(TYPE \*ivars, size_t nelems, const int \*status, int cmp, TYPE \*cmp_values)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the test set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with elements of `cmp_values`.

*cmp_values \[IN\]*  
Local address of an array of length `nelems` containing values to be compared with the respective objects in `ivars`. The type of `cmp_values` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_test_all_vector` routine indicates whether all entries in the test set specified by `ivars` and `status` have satisfied the test condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine does not block and returns zero if not all entries in `ivars` satisfied the test conditions. This routine compares each element of the `ivars` array in the test set with each respective value in `cmp_values` according to the comparison operator `cmp` at the calling PE. If `nelems` is 0, the test set is empty and this routine returns 1.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the test set. Elements of `status` set to 0 will be included in the test set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the test set is empty and this routine returns 0. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the test set. The `ivars`, `indices`, and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_test_all_vector` does not return 1 before the update of the memory indicated by `ivars` is fully complete.

**Returns**

`nvshmem_test_all_vector` returns 1 if all variables in `ivars` satisfy the test conditions or if `nelems` is 0, otherwise this routine returns 0.

<a id="nvshmem-test-any-vector"></a>

## **NVSHMEM_TEST_ANY_VECTOR**
\_\_device\_\_ size_t nvshmem_TYPENAME_test_any_vector(TYPE \*ivars, size_t nelems, const int \*status, int cmp, TYPE \*cmp_values)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the test set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with elements of `cmp_values`.

*cmp_values \[IN\]*  
Local address of an array of length `nelems` containing values to be compared with the respective objects in `ivars`. The type of `cmp_values` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_test_any_vector` routine indicates whether any entry in the test set specified by `ivars` and `status` has satisfied the test condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine does not block and returns `SIZE_MAX` if no entries in `ivars` satisfied the test condition. This routine compares each element of the `ivars` array in the test set with each respective value in `cmp_values` according to the comparison operator `cmp` at the calling PE. The order in which these elements are tested is unspecified. If an entry \\i\\ in `ivars` within the test set satisfies the test condition, a series of calls to `nvshmem_test_any_vector` must eventually return \\i\\.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the test set. Elements of `status` set to 0 will be included in the test set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the test set is empty and this routine returns `SIZE_MAX`. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the test set. The `ivars` and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_test_any_vector` does not return an index before the update of the memory indicated by the corresponding `ivars` element is fully complete.

**Returns**

`nvshmem_test_any_vector` returns the index of an element in the `ivars` array that satisfies the test condition. If the test set is empty or no conditions in the test set are satisfied, this routine returns `SIZE_MAX`.

<a id="nvshmem-test-some-vector"></a>

## **NVSHMEM_TEST_SOME_VECTOR**
\_\_device\_\_ size_t nvshmem_TYPENAME_test_some_vector(TYPE \*ivars, size_t nelems, size_t \*indices, const int \*status, int cmp, TYPE \*cmp_values)  

where *TYPE* is one of the standard AMO types and has a corresponding *TYPENAME* specified by Table [Standard AMO Types and Names](amo.html#stdamotypes), or *TYPE* is one of the signal types and has a corresponding *TYPENAME* specified by Table [Signal Types and Names](signal.html#signaltypes).

*ivars \[IN\]*  
Symmetric address of an array of remotely accessible data objects. The type of `ivars` should match that implied in the SYNOPSIS section.

*nelems \[IN\]*  
The number of elements in the `ivars` array.

*indices \[OUT\]*  
Local address of an array of indices of length at least `nelems` into `ivars` that satisfied the test condition.

*status \[IN\]*  
Local address of an optional mask array of length `nelems` that indicates which elements in `ivars` are excluded from the test set.

*cmp \[IN\]*  
A comparison operator from Table [\[p2p-consts\]](#p2p-consts) that compares elements of `ivars` with elements of `cmp_values`.

*cmp_values \[IN\]*  
Local address of an array of length `nelems` containing values to be compared with the respective objects in `ivars`. The type of `cmp_values` should match that implied in the SYNOPSIS section.

**Description**

The `nvshmem_test_some_vector` routine indicates whether at least one entry in the test set specified by `ivars` and `status` satisfies the test condition at the calling PE. The `ivars` objects at the calling PE may be updated by an AMO performed by a thread located within the calling PE or within another PE. This routine does not block and returns zero if no entries in `ivars` satisfied the test condition. This routine compares each element of the `ivars` array in the test set with each respective value in `cmp_values` according to the comparison operator `cmp` at the calling PE. This routine tests all elements of `ivars` in the test set at least once, and the order in which the elements are tested is unspecified.

Upon return, the `indices` array contains the indices of the elements in the test set that satisfied the test condition during the call to `nvshmem_test_some_vector`. The return value of `nvshmem_test_some_vector` is equal to the total number of these satisfied elements. If the return value is \\N\\, then the first \\N\\ elements of the `indices` array contain those unique indices that satisfied the test condition. These first \\N\\ elements of `indices` may be unordered with respect to the corresponding indices of `ivars`. The array pointed to by `indices` must be at least `nelems` long. If an entry \\i\\ in `ivars` within the test set satisfies the test condition, a series of calls to `nvshmem_test_some_vector` must eventually include \\i\\ in the `indices` array.

The optional `status` is a mask array of length `nelems` where each element corresponds to the respective element in `ivars` and indicates whether the element is excluded from the test set. Elements of `status` set to 0 will be included in the test set, and elements set to a nonzero value will be ignored. If all elements in `status` are nonzero or `nelems` is 0, the test set is empty and this routine returns 0. If `status` is a null pointer, it is ignored and all elements in `ivars` are included in the test set. The `ivars`, `indices`, and `status` arrays must not overlap in memory.

Implementations must ensure that `nvshmem_test_some_vector` does not return indices before the updates of the memory indicated by the corresponding `ivars` elements are fully complete.

**Returns**

`nvshmem_test_some_vector` returns the number of indices returned in the `indices` array. If the test set is empty, this routine returns 0.

<a id="nvshmem-signal-wait-until"></a>

## **NVSHMEM_SIGNAL_WAIT_UNTIL**
uint64_t nvshmemx_signal_wait_until_on_stream(

*uint64_t \*sig_addr*,

*int cmp*,

*uint64_t cmp_val*,

*cudaStream_t stream*

)[\#](#c.nvshmemx_signal_wait_until_on_stream "Link to this definition")  

\_\_device\_\_ uint64_t nvshmem_signal_wait_until(uint64_t \*sig_addr, int cmp, uint64_t cmp_val)  

&nbsp;

*sig_addr \[IN\]*  
Local address of the source signal variable.

*cmp \[IN\]*  
The comparison operator that compares `sig_addr` with `cmp_val`.

*cmp_val \[IN\]*  
The value against which the object pointed to by `sig_addr` will be compared.

**Description**

The `nvshmem_signal_wait_until` operation blocks until the value contained in the signal data object, `sig_addr`, at the calling PE satisfies the wait condition. In an NVSHMEM program with single-threaded or multithreaded PEs, the `sig_addr` object at the calling PE is expected only to be updated as a signal, through the signaling operations available in Section [NVSHMEM_PUT_SIGNAL](signal.html#subsec-shmem-put-signal) and Section [NVSHMEM_PUT_SIGNAL_NBI](signal.html#subsec-shmem-put-signal-nbi).

This routine can be used to implement point-to-point synchronization between PEs or between threads within the same PE. A call to this routine blocks until the value of `sig_addr` at the calling PE satisfies the wait condition specified by the comparison operator, `cmp`, and comparison value, `cmp_val`.

Implementations must ensure that `nvshmem_signal_wait_until` does not return before the update of the memory indicated by `sig_addr` is fully complete.

**Returns**

Return the contents of the signal data object, `sig_addr`, at the calling PE that satisfies the wait condition.

[](collectives.html "previous page")

previous

Collective Communication

[](ordering.html "next page")

next

Memory Ordering

On this page

- [**NVSHMEM_WAIT_UNTIL**](#nvshmem-wait-until)
  - [`nvshmemx_TYPENAME_wait_until_on_stream()`](#c.nvshmemx_TYPENAME_wait_until_on_stream)
  - [`nvshmemx_TYPENAME_wait_on_stream()`](#c.nvshmemx_TYPENAME_wait_on_stream)
- [**NVSHMEM_WAIT_UNTIL_ALL**](#nvshmem-wait-until-all)
- [**NVSHMEM_WAIT_UNTIL_ANY**](#nvshmem-wait-until-any)
- [**NVSHMEM_WAIT_UNTIL_SOME**](#nvshmem-wait-until-some)
- [**NVSHMEM_WAIT_UNTIL_ALL_VECTOR**](#nvshmem-wait-until-all-vector)
- [**NVSHMEM_WAIT_UNTIL_ANY_VECTOR**](#nvshmem-wait-until-any-vector)
- [**NVSHMEM_WAIT_UNTIL_SOME_VECTOR**](#nvshmem-wait-until-some-vector)
- [**NVSHMEM_TEST**](#nvshmem-test)
- [**NVSHMEM_TEST_ALL**](#nvshmem-test-all)
- [**NVSHMEM_TEST_ANY**](#nvshmem-test-any)
- [**NVSHMEM_TEST_SOME**](#nvshmem-test-some)
- [**NVSHMEM_TEST_ALL_VECTOR**](#nvshmem-test-all-vector)
- [**NVSHMEM_TEST_ANY_VECTOR**](#nvshmem-test-any-vector)
- [**NVSHMEM_TEST_SOME_VECTOR**](#nvshmem-test-some-vector)
- [**NVSHMEM_SIGNAL_WAIT_UNTIL**](#nvshmem-signal-wait-until)
  - [`nvshmemx_signal_wait_until_on_stream()`](#c.nvshmemx_signal_wait_until_on_stream)
