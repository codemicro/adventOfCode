import System.Environment
import System.Exit
import System.IO
import Data.Maybe
import Data.Char
import Control.Exception

type ChallengeReturn = Int

parse :: String -> [String]
parse = lines

one :: String -> ChallengeReturn
one inp = foldl
    (\acc line ->
        let digits = map (\x -> ord x - ord '0') (filter isDigit line) in
            assert ((length digits) /= 0) (
                acc + ((digits!!0) * 10) + (digits!!((length digits) - 1))
            )
    )
    0
    (parse inp)

two :: String -> ChallengeReturn
two inp = undefined

main :: IO ()
main = do args <- getArgs
          inp <- getContents
          _runFn (_selectFn args) inp

_selectFn :: [String] -> Maybe (String -> ChallengeReturn)
_selectFn ["1"] = Just one
_selectFn ["2"] = Just two
_selectFn _ = Nothing

_runFn :: Maybe (String -> ChallengeReturn) -> String -> IO ()
_runFn Nothing _ = _debug "Missing or invalid day argument" >> exitWith (ExitFailure 1)
_runFn (Just fn) inp = putStrLn (show (fn inp)) >> exitWith ExitSuccess

_debug :: String -> IO ()
_debug x = do hPutStrLn stderr x
